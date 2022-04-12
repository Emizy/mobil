from django.urls import path, re_path
from core.views.administrator import *
from core.views.invite import InviteView
from core.views.quotations import QuotationView, QuotationDetailView, QuotationDetailCopy

urlpatterns = [
    path('dashboard/', MainView.as_view(), name='admin'),
    re_path('service-stations/', ServiceStationsView.as_view(), name='stations'),
    re_path('suppliers/', SupplierView.as_view(), name='suppliers'),
    re_path('invitation/(?P<type>[^/]+)/', InviteView.as_view(), name='invitation'),
    re_path('quotations/(?P<type>[^/]+)/', QuotationView.as_view(), name='main-quotations'),
    path('quotations-copy/', QuotationDetailCopy.as_view(), name='main-quotations-copy'),
    re_path('quotations-preview/(?P<type>[^/]+)/(?P<id>[^/]+)', QuotationDetailView.as_view(),
            name='main-preview-quotations'),
]
