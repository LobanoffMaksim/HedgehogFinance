from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bond.urls')),
    path("portfolio/", include("portfolio.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

