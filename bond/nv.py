from bond.models import *
from bond.templatetags.report_tags import get_margin
from bond.templatetags.score_tags import *
from bond.config import *

from statistics import mean, median


def set_default_nv():
    """
    Legacy
    :return:
    """
    nv = NormalValues.objects.get_or_create()[0]
    for industry in Industry.objects.all():
        if industry.normal_values is None:
            industry.normal_values = nv
            industry.save()


def check_amortization(emitter):
    """
    :param emitter:
    :return: if amortization have been calculated by formula not from reports.
    """
    if abs(int(emitter[('rsbu', 'non-current-assets', 'LTM')] * 0.0906) - emitter[
        ('rsbu', 'amortization', 'LTM')]) < 500000:
        return False
    else:
        return True


def get_amortization_percentage(sector):
    amortization_percentage = []
    for emitter in sector.emitter_set.filter(need_add_fin_data=1):

        if check_amortization(emitter) and emitter[('rsbu', 'fixed-assets', 'LTM')] != 0\
                and emitter.report_data_level == 3:

            for year in emitter.interesting_years('rsbu'):
                if emitter[('rsbu', 'fixed-assets', year)] == 0:
                    continue
                x = emitter[('rsbu', 'amortization', year)] / \
                    (emitter[('rsbu', 'fixed-assets', year)] + emitter[('rsbu', 'intangible-assets', year)])
                if x < 1:
                    amortization_percentage.append(x)
    return amortization_percentage


def set_amortization(sector, avg):
    """
    Set amortization in sector as (fixed-assets + intangible-assets) * avg
    :param sector:
    :param avg: average percentage
    :return:
    """
    for emitter in sector.emitter_set.filter(need_add_fin_data=1):
        if emitter.report_data_level != 3:
            for year in emitter.interesting_years('rsbu'):
                x = emitter[('rsbu', 'fixed-assets', year)] + emitter[('rsbu', 'intangible-assets', year)]
                if x == 0:
                    x = emitter[('rsbu', 'non-current-assets', year)]
                if x == 0:
                    continue
                fi = emitter.finindicator_set.get(report_type='rsbu', type='amortization', year=year)
                fi.value = int(x * avg)
                fi.save()


def calc_amortization():
    """
    Calculating amortization as median percent of fixed-assets in sector.
    :return:
    """
    for sector in Sector.objects.all():
        amortization_percentage = get_amortization_percentage(sector)

        if amortization_percentage:
            set_amortization(sector, mean(amortization_percentage))


def get_bad_reports():
    """
    Finding unrepresentative reports.
    :return:
    """
    for emitter in Emitter.objects.filter(need_add_fin_data=1):
        if emitter.report_data_level == 0:
            continue

        if emitter[('rsbu', 'revenue', 'LTM')] < 10 ** 7 or len(emitter[('rsbu', 'revenue', 'all')]) < 2 or len(
                emitter[('rsbu', 'net-profit', 'all')]) < 2:
            print(1, emitter.title)
            emitter.is_report_ok = False
        elif emitter[('rsbu', 'net-profit', 'LTM')] / emitter[('rsbu', 'revenue', 'LTM')] > 0.8:
            print(2, emitter.title)
            emitter.is_report_ok = False
        elif emitter.credit_level is not None and emitter.credit_level >= 17 and emitter[
            ('rsbu', 'revenue', 'LTM')] < 5 * 10 ** 9:
            print(3, emitter.title)
            emitter.is_report_ok = False
        elif emitter.sector is not None and emitter.sector.id in [68, 56, 50, 80]:
            print(4, emitter.title)
            emitter.is_report_ok = False
        emitter.save()


def get_values_of_fin_metric(emitter, report_type, title, year):
    if emitter[(report_type, 'revenue', 'LTM')] == 0 or emitter[(report_type, title, 'LTM')] == 0:
        return []
    if year == 'all':
        ans = []
        for val in emitter[(report_type, title, year)]:
            if val == 0:
                continue
            ans.append(val)
        return ans
    else:
        return [emitter[(report_type, title, year)]]


def get_median_value(report_type, type, year):
    """
    Calculating median value of this fin metric in all sectors.
    :param report_type: 'RSBU' or 'IFRS'
    :param type: name of fin metric. Example "ebitda/revenue"
    :param year: year of calculating this metric. If year == 'all' it will be calculated for all years.
    :return:
    """
    for sector in Sector.objects.all():
        if sector.emitter_set.count() == 0:
            continue
        values = []

        for e in sector.emitter_set.filter(is_report_ok=True):
            values += get_values_of_fin_metric(e, report_type, type, year)

        if values:
            print(sector.title, median(values))


def get_emitters_set(sector, report_type):
    if report_type == 'ifrs':
        return sector.emitter_set.all()
    else:
        return sector.emitter_set.filter(is_report_ok=True)


def get_sectors(sectors):
    if sectors == 'all':
        return Sector.objects.all()
    else:
        return [sectors]


def update_all_median_values(report_type, sectors):
    """
    Updating all median values.
    :param report_type:
    :param sectors: 'all' if you want update all sectors. Sector object if you want to update only 1.
    :return:
    """

    for type, year in fin_metrics:
        for sector in get_sectors(sectors):
            if sector.emitter_set.count() == 0:
                continue

            MedianValue.objects.filter(report_type=report_type, sector=sector, title=type).delete()

            values = []
            for e in get_emitters_set(sector, report_type):
                values += get_values_of_fin_metric(e, report_type, type, year)

            if values:
                print(type, sector.title, round(median(values), 2))
                mv = MedianValue(report_type=report_type, sector=sector, title=type, value=round(median(values), 2))
                mv.save()


def calc_all_scores():
    """
    Calcs average score for all credit ratings.
    :return:
    """
    ans = []
    for e in Emitter.objects.filter(is_report_ok=True, report_data_level=3):
        scores = get_all_scores(e, 'rsbu')
        score = sum(scores[1:]) * scores[0] / 100
        ans.append([score, e.moex_id])
    ans.sort()
    s = [0 for _ in range(22)]
    cnt = [0 for _ in range(22)]
    for score, moex_id in ans:
        e = Emitter.objects.get(moex_id=moex_id)
        if e.credit_level is not None:
            s[e.credit_level] += score
            cnt[e.credit_level] += 1
    for i in range(22):
        if cnt[i] != 0:
            print(credit_ratings[i], s[i] / cnt[i])
