from django.contrib import admin
from django.urls import include, path

from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/', include('accounts.urls')),

    path('localevents/', include('localevents.urls')),
    path('bookclub/', include('bookclub.urls')),
    path('commissions/', include('commissions.urls')),
    path('diyprojects/', include('diyprojects.urls')),
    path('merchstore/', include('merchstore.urls')),
]