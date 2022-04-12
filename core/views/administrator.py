from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required

from station.models import ServiceStation
from supplier.models import SupplierAccount
from utils.base import BaseView
from core.models.quotations import SupplierQuotations


class MainView(View):
    def get(self, request):
        pending_quotation = SupplierQuotations.objects.filter(status='PENDING').count()
        all_quotation = SupplierQuotations.objects.all().count()
        total_service_station = ServiceStation.objects.all().count()
        total_supplier = SupplierAccount.objects.all().count()
        return render(request, 'main/dashboard.html', {'supplier': total_supplier,
                                                       'station': total_service_station,
                                                       'pending': pending_quotation,
                                                       'all_quotation':all_quotation})


@method_decorator(login_required, name='dispatch')
class ServiceStationsView(BaseView):
    def get(self, request, *args, **kwargs):
        try:
            stations = ServiceStation.objects.filter(company=self.get_user_company())
            return render(request, 'main/stations.html', {'stations': stations})
        except Exception as ex:
            print(ex)
            pass


@method_decorator(login_required, name='dispatch')
class SupplierView(BaseView):
    def get(self, request, *args, **kwargs):
        try:
            suppliers = SupplierAccount.objects.filter(company=self.get_user_company())
            return render(request, 'main/supplier.html', {'suppliers': suppliers})
        except Exception as ex:
            print(ex)
