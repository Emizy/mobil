from django.urls import path, re_path
from station.views.quotation import *
from station.views.dashboard import *

urlpatterns = [
    path('dashboard/', MainView.as_view(), name='station-dashboard'),
    path('quotation/', QuotationView.as_view(), name='station-quotation'),
    path('create-quotation/', CreateQuotation.as_view(), name='station-create-quotation'),
]
