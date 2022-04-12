from django.urls import path, re_path
from supplier.views.dashboard import *
from supplier.views.quotation import QuotationView, CreateQuotation
from supplier.views.branch import BranchView, CreateBranchView

urlpatterns = [
    path('dashboard/', MainView.as_view(), name='supplier-dashboard'),
    path('quotation/', QuotationView.as_view(), name='supplier-quotation'),
    path('create-quotation/', CreateQuotation.as_view(), name='supplier-create-quotation'),
    path('branch/', BranchView.as_view(), name='supplier-branch'),
    path('create-branch/', CreateBranchView.as_view(), name='supplier-create-branch'),
]
