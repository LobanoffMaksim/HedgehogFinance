from django.urls import path


from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('add-finfile/', add_finfile, name='add_finfile'),
    path('thanks/', thanks, name='thanks'),
    path('bond_screener/', bond_screener2, name='bond_screener'),
    path('bond/<str:isin>/', bond_data, name='bond'),
    path('risk-chart/<int:level>/', rick_chart, name='rick_chart'),
    path('fast_update/', view_fast_update, name='fast_update'),
    path('update_all_bonds/', view_update_all_bonds, name='update_all_bonds'),
]
