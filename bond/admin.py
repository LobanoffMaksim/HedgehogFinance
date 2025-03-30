from abc import ABC

from django.contrib import admin

from .models import *


class CouponAdmin(admin.ModelAdmin):
    list_display = ('type', 'size', 'aci', 'period', 'sum', )


class BondAdmin(admin.ModelAdmin):
    list_display = ('title', 'isin', 'facevalue', 'end_date', )
    readonly_field = ( 'isin', )
    list_filter = ('is_for_qualified_investors', 'isin', )


class IsSectorNull(admin.SimpleListFilter):
    title = 'is_sector_null'
    parameter_name = 'is_sector_null'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(sector__isnull=True)
        elif value == 'No':
            return queryset.exclude(sector__isnull=True)
        return queryset


class EmitterAdmin(admin.ModelAdmin):
    list_display = ('inn', 'title', 'is_report_ok', 'e_id', 'sector', 'need_add_fin_data', 'report_data_level')
    list_filter = (IsSectorNull, 'ifrs_exists', 'is_report_ok', 'sector__title', 'need_add_fin_data', 'report_data_level', 'title')
    readonly_fields = ('moex_id', )
    list_editable = ('title', 'is_report_ok', 'sector', 'need_add_fin_data', 'report_data_level', )
    ordering = ('moex_id', )


class NormalValuesAdmin(admin.ModelAdmin):
    list_display = ('title', 'net_margin1', 'operation_margin1', 'ebitda_margin1', )
    readonly_fields = ('title',)

    ordering = ('id',)


class FinIndicatorAdmin(admin.ModelAdmin):
    list_display = ('emitter', 'type', 'value', 'year', 'report_type', )
    list_editable = ('value',)
    list_filter = ('year', 'type', 'report_type', 'emitter')
    ordering = ('-id',)


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'order_id')
    list_editable = ('order_id', )


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bond', 'date', 'type')
    list_filter = ('bond', 'type', )


class ReportLinkAdmin(admin.ModelAdmin):
    list_display = ('emitter', 'link', )


class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'risk_level', 'emitter_num')
    list_editable = ('title', 'risk_level', )
    ordering = ('title', )

    @admin.display(empty_value="???")
    def emitter_num(self, obj):
        return obj.emitter_set.count()


class MedianValueAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'sector', 'title', 'value')
    list_editable = ('value', )
    list_filter = ('report_type', 'sector', 'title')


class CreditRatingAdmin(admin.ModelAdmin):
    list_display = ('emitter', 'agency', 'value')
    list_editable = ('value',)
    list_filter = ('agency', 'value', 'emitter')


class FinFileAdmin(admin.ModelAdmin):
    list_display = ('emitter', 'fin_file')
    list_filter = ('emitter', )


class ReportAdmin(admin.ModelAdmin):
    list_display = ('emitter', 'description', 'type', 'status', 'file_path', 'download_link')
    list_filter = ('type', 'status', 'emitter', )
    list_editable = ('status', )


admin.site.register(Coupon, CouponAdmin)
admin.site.register(Bond, BondAdmin)
admin.site.register(Emitter, EmitterAdmin)
admin.site.register(NormalValues, NormalValuesAdmin)
admin.site.register(FinIndicator, FinIndicatorAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(ReportLink, ReportLinkAdmin)
admin.site.register(MedianValue, MedianValueAdmin)
admin.site.register(CreditRating, CreditRatingAdmin)
admin.site.register(EmitterFinFile, FinFileAdmin)
admin.site.register(Report, ReportAdmin)