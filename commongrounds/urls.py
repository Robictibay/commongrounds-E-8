from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'), 
    
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/', include('accounts.urls')),            
    
    path('localevents/', include('localevents.urls')),
    path('merchstore/', include('merchstore.urls')),
    path('bookclub/', include('bookclub.urls')),
    path('diyprojects/', include('diyprojects.urls')),
    path('commissions/', include('commissions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)