from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from core.models.quotations import SupplierQuotations
from supplier.models import SupplierAccount, Branch
from utils.base import BaseView


@method_decorator(login_required, 'dispatch')
class MainView(BaseView):
    def get(self, request):
        supplier = SupplierAccount.objects.filter(user=request.user).first()
        quotes = SupplierQuotations.objects.filter(branch__supplier=supplier)
        branches = Branch.objects.filter(supplier=supplier)
        paid_quotes = SupplierQuotations.objects.filter(branch__supplier=supplier, status='APPROVED').aggregate(
            total=Sum('amount'))
        return render(request, 'supplier/index.html',
                      {'quotes': quotes.count(), 'paid_quotes': paid_quotes['total'] if paid_quotes['total'] else 0,
                       'branches': branches.count()})
