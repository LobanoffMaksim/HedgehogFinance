from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .forms import EmitterFinFileForm, EmitterInfoForm, EmitterFinFileBoNalogForm, BondScreenerForm
from .emitter import upload_finfile
from .models import Bond, Emitter
from .config import conv_agency, credit_ratings
from .moex import fast_update, update_all_bonds

from datetime import datetime, timedelta
from fuzzywuzzy import process


def page_404(request, exception=None):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def credit_rating_list(emitter):
    """
    Getting all credit ratings.
    """
    ans = []
    for cr in emitter.creditrating_set.all():
        ans.append((conv_agency[cr.agency], cr.value))
    return ans


def get_report_type(request, emitter):
    if request.method == 'GET' and ('report_type' in request.GET):
        if request.GET['report_type'] not in ['rsbu', 'ifrs']:
            return '404'
        else:
            return request.GET['report_type']
    else:
        if emitter[('ifrs', 'assets', 'LTM')] > 1000000:
            return 'ifrs'
        return 'rsbu'


def get_emitter_info_exists(report_type, emitter):
    if emitter[(report_type, 'assets', 'LTM')] > 1000000 and (report_type == 'ifrs' or emitter.is_report_ok):
        return 2
    if emitter.description is not None:
        return 1
    return 0


def get_view_file(report_type, emitter, emitter_info_exists):
    if emitter_info_exists <= 1:
        return 'bond/bond_view.html'
    if emitter.report_data_level == 5:
        return 'bond/bond_view2.html'
    elif report_type == 'ifrs' or emitter.report_data_level != 3:
        return 'bond/bond_view.html'
    else:
        return 'bond/bond_view2.html'

# @cache_page(86400)
def bond_data(request, isin):
    """
    Loads page about bond.
    """
    if request.method == 'GET' and ('search_isin' in request.GET) and request.GET['search_isin'] != isin and \
            request.GET['search_isin'] != '':
        url = reverse_lazy('bond', kwargs={'isin': request.GET['search_isin']})
        return HttpResponseRedirect(url)

    # bond = get_object_or_404(Bond, isin=isin)
    bond = Bond.objects.prefetch_related("emitter__finindicator_set").get(isin=isin)
    emitter = Emitter.objects.prefetch_related("finindicators")
    report_type = get_report_type(request, bond.emitter)
    if report_type  == '404':
        return page_404(request)
    emitter_info_exists = get_emitter_info_exists(report_type, bond.emitter)
    ceo = bond.emitter.ceo
    cr = credit_rating_list(bond.emitter)
    file_view = get_view_file(report_type, bond.emitter, emitter_info_exists)
    return render(request, file_view, {'bond': bond,
                                       'emitter': emitter,
                                       'ceo': ceo,
                                       'report_type': report_type,
                                       'emitter_info_exists': emitter_info_exists,
                                       'cr': cr,
                                       "cr_size": len(cr)})


def index(request):
    """
    Loads main page
    """
    if request.method == 'GET' and ('search_isin' in request.GET) and request.GET['search_isin'] != '':
        url = reverse_lazy('bond', kwargs={'isin': request.GET['search_isin']})
        return HttpResponseRedirect(url)
    return render(request, 'bond/index.html')


def add_finfile(request):
    """
    Loads page for adding files with report data
    :param request:
    :return:
    """
    if request.method == 'GET' and ('search_isin' in request.GET) and request.GET['search_isin'] != '':
        url = reverse_lazy('bond', kwargs={'isin': request.GET['search_isin']})
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        form = EmitterFinFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_finfile(form.cleaned_data['updated_by'], form.cleaned_data['fin_file'])
            return HttpResponseRedirect('/thanks/')

    else:
        form = EmitterFinFileForm()

    return render(request, 'bond/addfinfile.html', {'form': form})


def thanks(request):
    if request.method == 'GET' and ('search_isin' in request.GET) and request.GET['search_isin'] != '':
        url = reverse_lazy('bond', kwargs={'isin': request.GET['search_isin']})
        return HttpResponseRedirect(url)
    return HttpResponse('Успешно!')


def get_simple_bonds_list():
    """
    Getting default bonds list.
    :return:
    """
    bonds = Bond.objects.all()
    today = datetime.now().date()
    bonds = bonds.filter(end_date__gte=today)
    bonds = bonds.order_by('-yield_to_maturity')
    return bonds


def get_start_bonds_list():
    """
    Getting bonds list with start filters.
    TO DO: it causes a lot of bugs.
    :return:
    """
    bonds = Bond.objects.all()
    today = datetime.now().date()
    bonds = bonds.filter(end_date__gte=today + timedelta(days=20))
    bonds = bonds.filter(coupon__sum__gte=1)
    bonds = bonds.filter(price__gte=70)
    bonds = bonds.filter(liquidity__gte=1000000)
    bonds = bonds.order_by('-yield_to_maturity')
    return bonds


def get_bonds_list(data):
    """
    Filtering bonds according to for. New version.
    :param data:
    :return:
    """
    bonds = get_simple_bonds_list()
    print(333)

    if data["credit_level_min"] is not None and data["credit_level_min"] != "Не важен" and data[
        "credit_level_min"] != "":

        credit_level = credit_ratings.index(data["credit_level_min"])
        bonds = bonds.filter(emitter__credit_level__gte=credit_level)
    if data["mat_yield_min"] is not None:
        bonds = bonds.filter(yield_to_maturity__gte=data["mat_yield_min"])
    if data["mat_yield_max"] is not None:
        bonds = bonds.filter(yield_to_maturity__lte=data["mat_yield_max"])
    if data["liquidity_min"] is not None:
        bonds = bonds.filter(liquidity__gte=data["liquidity_min"] * 1000000)
    if data["coupon_size_min"] is not None:
        bonds = bonds.filter(coupon__sum__gt=data["coupon_size_min"])
    if data["coupon_size_max"] is not None:
        bonds = bonds.filter(coupon__sum__lt=data["coupon_size_max"])
    if data["price_min"] is not None:
        bonds = bonds.filter(price__gte=data["price_min"])
    if data["price_max"] is not None:
        bonds = bonds.filter(price__lte=data["price_max"])

    today = datetime.now().date()
    if data["d_before_end_min"] is not None:
        end_date_min = today + timedelta(days=data["d_before_end_min"])
        bonds = bonds.filter(end_date__gte=end_date_min)
    if data["d_before_end_max"] is not None:
        end_date_max = today + timedelta(days=data["d_before_end_max"])
        bonds = bonds.filter(end_date__lte=end_date_max)
    if data['search_title'] is not None and data['search_title'] != '':
        titles = [bond.title for bond in bonds]
        need_titles = [title for title, sctore in process.extract(data['search_title'], titles, limit=15)]

        bonds = bonds.filter(title__in=need_titles)
        for bond in bonds:
            bond.order_id = need_titles.index(bond.title)
            bond.save()
        bonds = bonds.order_by('order_id')
    else:
        bonds = bonds.order_by('-yield_to_maturity')
    paginator = Paginator(bonds, 100)

    page_obj = paginator.get_page(data["page"])
    return page_obj


def bond_screener2(request):
    """
    Loads page with bond screener. New version
    :param request:
    :return:
    """
    if request.method == 'GET' and ('search_isin' in request.GET) and request.GET['search_isin'] != '':
        url = reverse_lazy('bond', kwargs={'isin': request.GET['search_isin']})
        return HttpResponseRedirect(url)
    if request.method == "POST":

        form = BondScreenerForm(request.POST)

        if form.is_valid():
            return render(request, "bond/bond_screener2.html", {"form": form,
                                                                "bonds": get_bonds_list(form.cleaned_data),
                                                                "is_form_default": False})
        else:
            return render(request, "bond/bond_screener2.html", {"form": form,
                                                                "bonds": Paginator(get_start_bonds_list(),
                                                                                   100).get_page(1),
                                                                "is_form_default": False})

    else:

        form = BondScreenerForm(initial={"page": 1,
                                         "d_before_end_min": 20,

                                         })
        # form.initial = True

        bonds = get_start_bonds_list()

        return render(request, "bond/bond_screener2.html", {"form": form,
                                                            "bonds": Paginator(bonds, 100).get_page(1),
                                                            "is_form_default": True})


def rick_chart(request, level):
    """
    Loads risk chart.
    :param request:
    :param level:
    :return:
    """
    return render(request, "bond/risk_chart.html", {
        "title": f'{level}/10',
        "level": level,
    })


def view_fast_update(request):
    fast_update()
    return HttpResponse('Успешно!')


def view_update_all_bonds(request):
    update_all_bonds(1, 1)
    return HttpResponse('Успешно!')
