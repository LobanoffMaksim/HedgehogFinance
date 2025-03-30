from django.db import models
from bond.config import interesting_years_LTM
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class PaymentType(models.Model):
    title = models.CharField(max_length=40)
    order_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class CouponType(models.Model):
    title = models.CharField(max_length=40)


class Coupon(models.Model):
    type = models.ForeignKey(CouponType, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, )
    size = models.FloatField()
    aci = models.FloatField()
    period = models.SmallIntegerField()
    sum = models.FloatField(blank=True, null=True, )


class NormalValues(models.Model):
    title = models.CharField(max_length=50, default='все')
    net_margin1 = models.FloatField(default=15)
    net_margin2 = models.FloatField(default=7.5)
    operation_margin1 = models.FloatField(default=18)
    operation_margin2 = models.FloatField(default=9)
    ebitda_margin1 = models.FloatField(default=20)
    ebitda_margin2 = models.FloatField(default=10)

    roa1 = models.FloatField(default=10)
    roa2 = models.FloatField(default=5)
    roe1 = models.FloatField(default=15)
    roe2 = models.FloatField(default=7.5)
    nd_to_ebitda1 = models.FloatField(default=2)
    nd_to_ebitda2 = models.FloatField(default=4)
    nd_to_equity1 = models.FloatField(default=1)
    nd_to_equity2 = models.FloatField(default=2)
    interest_ratio1 = models.FloatField(default=33)
    interest_ratio2 = models.FloatField(default=66)
    equity_level1 = models.FloatField(default=16)
    equity_level2 = models.FloatField(default=8)
    cur_liquidity1 = models.FloatField(default=1.5)
    cur_liquidity2 = models.FloatField(default=0.75)
    fast_liquidity1 = models.FloatField(default=1.00)
    fast_liquidity2 = models.FloatField(default=0.50)
    absolute_liquidity1 = models.FloatField(default=0.20)
    absolute_liquidity2 = models.FloatField(default=0.10)


class Industry(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Sector(models.Model):
    title = models.CharField(max_length=50)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    risk_level = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title


class EmitterFinFile(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=20)
    fin_file = models.FileField(upload_to='uploads/emitters/')


class Emitter(models.Model):
    title = models.CharField(null=True, max_length=52)
    moex_id = models.IntegerField(unique=True, )
    description = models.TextField(blank=True, null=True, )
    normal_values = models.ForeignKey(NormalValues, on_delete=models.SET_NULL, null=True)
    ceo = models.CharField(blank=True, null=True, max_length=48)
    sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.CASCADE)
    website1 = models.URLField(blank=True, null=True, )
    website2 = models.URLField(blank=True, null=True, )
    e_id = models.IntegerField(blank=True, null=True, )
    ls_link = models.URLField(blank=True, null=True, )
    okpo = models.IntegerField(blank=True, null=True, )
    inn = models.IntegerField(blank=True, null=True, )
    is_system_important = models.BooleanField(blank=True, null=True, )
    akra = models.CharField(blank=True, null=True, max_length=8)
    fitch = models.CharField(blank=True, null=True, max_length=8)
    ra_expert = models.CharField(blank=True, null=True, max_length=8)
    sp = models.CharField(blank=True, null=True, max_length=8)
    credit_level = models.IntegerField(blank=True, null=True)
    moodys = models.CharField(blank=True, null=True, max_length=8)
    netdebt_to_ebitda = models.FloatField(blank=True, null=True, )
    netdebt_to_equity = models.FloatField(blank=True, null=True, )
    netdebt_to_assets = models.FloatField(blank=True, null=True, )
    revenue = models.BigIntegerField(null=True, blank=True, )
    updated_by = models.CharField(null=True, blank=True, max_length=20)
    fin_data = models.JSONField(null=True, blank=True, )
    need_add_fin_data = models.BooleanField(default=False)
    fin_file = models.OneToOneField(EmitterFinFile, null=True, blank=True, on_delete=models.CASCADE, )
    report_data_level = models.SmallIntegerField(null=True, blank=True, default=0)
    is_report_ok = models.BooleanField(null=True, blank=True, default=True)
    ifrs_exists = models.BooleanField(null=True, blank=True, default=False)

    def get_example_bond(self):
        return Bond.objects.filter(moex_id=self.moex_id).first()

    def interesting_years(self, report_type):
        ans = []
        for year in interesting_years_LTM:
            if self[(report_type, 'revenue', year)] > 1000000:
                ans.append(year)
        return ans

    def prev_year(self, report_type, year):
        all = self.interesting_years(report_type)
        return all[all.index(year) - 1]

    class Meta:
        ordering = ['updated_by', '-revenue']

    def __getitem__(self, data):

        report_type, title, year = data
        if year == 'all':
            ans = []
            if 'turnover' not in title:
                for cur_year in self.interesting_years(report_type):
                    ans.append(self[(report_type, title, cur_year)])
            else:
                for cur_year in self.interesting_years(report_type)[1:]:
                    ans.append(self[(report_type, title, cur_year)])
            return ans
        else:
            if title == 'ebitda':
                return self[(report_type, 'ebt', year)] + \
                       self[(report_type, 'amortization', year)] + \
                       self[(report_type, 'interest-payable', year)] - \
                       self[(report_type, 'interest-receivable', year)]
            elif title == 'FCF':

                return self[(report_type, 'OCF', year)] - \
                       self[(report_type, 'CAPEX', year)]
            elif title == 'operation-expenses':
                return self[(report_type, 'revenue', year)] - \
                       self[(report_type, 'operation-profit', year)]
            elif title == 'fast_liquidity':
                return self[(report_type, 'cash', year)] + \
                       self[(report_type, 'accounts-receivable', year)]
            elif title == 'net_debt':
                return self[(report_type, 'short-debt', year)] + \
                       self[(report_type, 'long-debt', year)] - \
                       self[(report_type, 'cash', year)] - \
                       self[(report_type, 'escrow', year)]
            elif title == 'debt':
                return self[(report_type, 'short-debt', year)] + \
                       self[(report_type, 'long-debt', year)]
            elif title == 'financial-investments':
                return self[(report_type, 'financial-investments-long', year)] + \
                       self[(report_type, 'financial-investments-short', year)]
            elif title == 'liabilities':
                return self[(report_type, 'long-liabilities', year)] + \
                       self[(report_type, 'short-liabilities', year)]
            elif title == 'working-capital':
                return self[(report_type, 'current-assets', year)] - \
                       self[(report_type, 'short-liabilities', year)]
            elif title == 'operating-working-capital':
                return self[(report_type, 'current-assets', year)] - \
                       self[(report_type, 'financial-investments-short', year)] - \
                       self[(report_type, 'short-liabilities', year)] + \
                       self[(report_type, 'short-debt', year)]
            elif '/' in title:
                i = title.index('/')
                if self[(report_type, title[i+1:], year)] == 0:
                    return 0
                return self[(report_type, title[:i], year)] / \
                       self[(report_type, title[i+1:], year)]
            elif 'cagr' in title:
                year_num = int(title[5])
                type = title[7:]
                data = self[(report_type, type, 'all')]
                if len(data) >= 2 and data[-1] == data[-2]:
                    data.pop()
                if len(data) == 1:
                    return 0

                if len(data) < year_num + 1 and len(data) != 1:
                    year_num = len(data) - 1
                    print(year_num)
                if data[-year_num - 1] == 0:
                    return 0
                if data[-1] < 0:
                    return -100
                if data[-year_num - 1] < 0:
                    return 100
                return ((data[-1] / data[-year_num - 1]) ** (1 / year_num) - 1) * 100
            elif 'turnover' in title:
                type = title[9:]
                x = (self[(report_type, type, self.prev_year(report_type, year))] + self[(report_type, type, year)]) // 2
                if x == 0:
                    return 0
                return 365 / (self[(report_type, 'revenue', year)] / x)
            elif title == 'Altman-score':
                return 0.717 * self[(report_type, 'working-capital', year)] / self[(report_type, 'assets', year)] + \
                       0.847 * self[(report_type, 'retained-earnings', year)] / self[(report_type, 'assets', year)] + \
                       3.107 * self[(report_type, 'ebt', year)] / self[(report_type, 'assets', year)] + \
                       0.42 * self[(report_type, 'equity', year)] / max(1, self[(report_type, 'debt', year)]) + \
                       0.995 * self[(report_type, 'revenue', year)] / self[(report_type, 'assets', year)]
            elif title == 'Springate-score':
                return 1.03 * self[(report_type, 'working-capital', year)] / self[(report_type, 'assets', year)] + \
                       3.07 * self[(report_type, 'operation-profit', year)] / self[(report_type, 'assets', year)] + \
                       0.66 * self[(report_type, 'ebt', year)] / self[(report_type, 'short-liabilities', year)] + \
                       0.4 * self[(report_type, 'revenue', year)] / self[(report_type, 'assets', year)]
            elif title == 'Lis-score':
                return 0.063 * self[(report_type, 'working-capital', year)] / self[(report_type, 'assets', year)] + \
                       0.092 * self[(report_type, 'operation-profit', year)] / self[(report_type, 'assets', year)] + \
                       0.057 * self[(report_type, 'net-profit', year)] / self[(report_type, 'short-liabilities', year)] + \
                       0.0014 * self[(report_type, 'equity', year)] / self[(report_type, 'liabilities', year)]
            elif title == 'Taffler-score':
                return 3.2 + 12.18 * self[(report_type, 'ebt', year)] / self[(report_type, 'short-liabilities', year)] + \
                       2.5 * self[(report_type, 'current-assets', year)] / self[(report_type, 'liabilities', year)] - \
                       10.68 * self[(report_type, 'short-liabilities', year)] / self[(report_type, 'assets', year)] + \
                       0.0029 * 365 * self[(report_type, 'working-capital', year)] / self[(report_type, 'operation-expenses', year)]
            elif title == 'Zajceva-score':
                return 0.25 * self[(report_type, 'ebt', year)] / self[(report_type, 'equity', year)] + \
                       0.1 * self[(report_type, 'accounts-payable', year)] / self[(report_type, 'accounts-receivable', year)] + \
                       0.2 * self[(report_type, 'short-liabilities', year)] / (self[(report_type, 'financial-investments-short', year)] + self[(report_type, 'cash', year)]) + \
                       0.25 * self[(report_type, 'ebt', year)] / max(1, self[(report_type, 'revenue', year)]) + \
                       0.1 * self[(report_type, 'liabilities', year)] / self[(report_type, 'equity', year)] + \
                       0.1 * self[(report_type, 'assets', year)] / self[(report_type, 'revenue', year)]
            elif title == 'Zajceva-score-ok':
                return 1.57 + 0.1 * self[(report_type, 'assets', year)] / self[(report_type, 'revenue', year)]
            elif title == 'cnt-default-scores':
                ans = 0
                if self[(report_type, 'Altman-score', year)] < 1.23: ans += 1
                if self[(report_type, 'Springate-score', year)] < 0.865: ans += 1
                if self[(report_type, 'Lis-score', year)] < 0.037: ans += 1
                if self[(report_type, 'Taffler-score', year)] < 0: ans += 1
                if self[(report_type, 'Zajceva-score', year)] > \
                        self[(report_type, 'Zajceva-score-ok', self.prev_year(report_type, year))]: ans += 1

                return ans
            elif self.finindicator_set.filter(report_type=report_type, type=title, year=year).exists():
                return self.finindicator_set.get(report_type=report_type, type=title, year=year).value
            else:
                return 0

    def __str__(self):
        if self.title is not None:
            return self.title
        else:
            return '---'


class Bond(models.Model):
    isin = models.CharField(max_length=30, unique=True, )
    title = models.CharField(blank=True, null=True, max_length=100)
    price = models.FloatField(blank=True, null=True)
    start_facevalue = models.FloatField(blank=True, null=True)
    facevalue = models.FloatField(blank=True, null=True)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.CASCADE, )
    emitter = models.ForeignKey(Emitter, blank=True, null=True, on_delete=models.CASCADE, )
    coupon = models.OneToOneField(Coupon, blank=True, null=True, on_delete=models.CASCADE, )
    is_subordinated = models.BooleanField(blank=True, null=True, )
    issue_volume = models.BigIntegerField(blank=True, null=True, )
    placement_date = models.DateField(blank=True, null=True, )
    maturity_date = models.DateField(blank=True, null=True, )
    end_date = models.DateField(blank=True, null=True, )
    collateral = models.CharField(blank=True, null=True, max_length=100)
    liquidity = models.BigIntegerField(blank=True, null=True, default=1)
    moex_id = models.IntegerField(blank=True, null=True, )
    board = models.CharField(max_length=10, blank=True, null=True, )
    is_traded_in_TI = models.BooleanField(blank=True, null=True, )
    website = models.URLField(blank=True, null=True, )
    current_yield = models.FloatField(blank=True, null=True, )
    yield_to_maturity = models.FloatField(blank=True, null=True, )
    order_id = models.IntegerField(blank=True, null=True)
    is_for_qualified_investors = models.BooleanField(blank=True, null=True, )

    def __str__(self):
        return self.isin


class GuarantorType(models.Model):
    title = models.CharField(max_length=30)


class Guarantor(models.Model):
    type = models.ForeignKey(GuarantorType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    website = models.URLField()
    bond = models.ForeignKey(Bond, on_delete=models.CASCADE)


class Payment(models.Model):
    date = models.DateField()
    bond = models.ForeignKey(Bond, on_delete=models.CASCADE)
    size = models.FloatField()
    relative_size = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)


class FinIndicator(models.Model):
    emitter = models.ForeignKey(Emitter, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=4)
    type = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    value = models.BigIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['year']


class ReportLink(models.Model):
    emitter = models.ForeignKey(Emitter, on_delete=models.CASCADE)
    link = models.URLField()
    hash = models.IntegerField(null=True, blank=True)


class CreditRating(models.Model):
    emitter = models.ForeignKey(Emitter, on_delete=models.CASCADE)
    link = models.URLField(null=True, blank=True)
    agency = models.CharField(null=True, blank=True, max_length=30, default=None)
    value = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        ordering = ['id']


class MedianValue(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    value = models.FloatField()
    report_type = models.CharField(max_length=4, default='rsbu')


class Report(models.Model):
    class ReportStatus(models.TextChoices):
        START = 'ST', _('Start')
        DOWNLOADED = 'DW', _('Downloaded')
        UNZIPPED = 'UZ', _('Unzipped')
        IMAGED = 'IM', _('Imaged')
        PARSED = 'PR', _('Parsed')
        ERROR = 'ER', _('Error')

    emitter = models.ForeignKey(Emitter, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, default='rsbu')
    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.START
    )
    description = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    download_link = models.URLField(null=True, blank=True)
    reporting_period = models.CharField(max_length=8, null=True, blank=True)
    file_path = models.CharField(max_length=200, null=True, blank=True)
    unit_of_measurement = models.IntegerField(null=True, blank=True, default=1)
    images_dir = models.CharField(max_length=200, null=True, blank=True)
    raw_data = models.TextField(null=True, blank=True)

    first_significant_page = models.IntegerField(null=True, blank=True, default=None)
    last_significant_page = models.IntegerField(null=True, blank=True, default=None)



