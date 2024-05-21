from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('account/', include('profiles.urls')),
    path('basket/', include('basket.urls')),
    path('order/', include('orders.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
