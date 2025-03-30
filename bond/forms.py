from django.forms import Form
from django import forms
from .models import EmitterFinFile


class EmitterFinFileForm(forms.Form):
    updated_by = forms.CharField(max_length=20)
    fin_file = forms.FileField()


class EmitterFinFileBoNalogForm(forms.Form):
    user = forms.CharField(max_length=20)
    f2021 = forms.FileField()
    f2019 = forms.FileField(required=False)
    moex_id = forms.IntegerField()
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(required=False)
    ceo = forms.CharField(max_length=100, required=False)
    sector = forms.CharField(max_length=100, required=False)
    industry = forms.CharField(max_length=100, required=False)

    website1 = forms.CharField(max_length=100, required=False)
    website2 = forms.CharField(max_length=100, required=False)
    is_system_important = forms.BooleanField(required=False)
    akra = forms.CharField(max_length=20, required=False)
    fitch = forms.CharField(max_length=20, required=False)
    ra_expert = forms.CharField(max_length=20, required=False)
    sp = forms.CharField(max_length=20, required=False)
    moodys = forms.CharField(max_length=20, required=False)
    amortization2021 = forms.IntegerField()
    amortization2020 = forms.IntegerField()
    escrow2020 = forms.IntegerField()
    escrow2021 = forms.IntegerField()


class EmitterInfoForm(forms.Form):
    moex_id = forms.IntegerField()


class BondScreenerForm(forms.Form):
    mat_yield_min = forms.FloatField(required=False, initial=-1)
    mat_yield_max = forms.FloatField(required=False, initial=-1)
    d_before_end_min = forms.IntegerField(required=False, initial=20)
    d_before_end_max = forms.IntegerField(required=False, initial=-1)
    search_title = forms.CharField(max_length=100, required=False, initial=-1)
    credit_level_min = forms.ChoiceField(required=False, choices=[
        ('Не важен', 'Не важен'),
        ('B-', 'B-'),
        ('B', 'B'),
        ('B+', 'B+'),
        ('BB-', 'BB-'),
        ('BB', 'BB'),
        ('BB+', 'BB+'),
        ('BBB-', 'BBB-'),
        ('BBB', 'BBB'),
        ('BBB+', 'BBB+'),
        ('A-', 'A-'),
        ('A', 'A'),
        ('A+', 'A+'),
        ('AA-', 'AA-'),
        ('AA', 'AA'),
        ('AA+', 'AA+'),
        ('AAA', 'AAA'),
    ], initial="Не важен")
    liquidity_min = forms.FloatField(required=False, initial=-1)
    coupon_size_min = forms.FloatField(required=False, initial=-1)
    coupon_size_max = forms.FloatField(required=False, initial=-1)
    price_min = forms.FloatField(required=False, initial=-1)
    price_max = forms.FloatField(required=False, initial=-1)
    search_isin = forms.CharField(required=False, initial=-1)
    page = forms.IntegerField(required=False, initial=1)


