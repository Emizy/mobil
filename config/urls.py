from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from config import settings
from core.views import auth as auth_views
from core import urls as core_url
from station import urls as station_url
from supplier import url as supplier_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path('accept/(?P<type>[^/]+)/(?P<token>[^/]+)/', auth_views.AccessInvitationView.as_view(), name='accept'),
    path('administrator/', include(core_url)),
    path('station/', include(station_url)),
    path('supplier/', include(supplier_url)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
