from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from core.models.quotations import StationQuotations
from station.models import ServiceStation
from utils.base import BaseView


@method_decorator(login_required, 'dispatch')
class MainView(BaseView):
    def get(self, request):
        station = ServiceStation.objects.filter(user=request.user).first()
        total_quotation = StationQuotations.objects.filter(station=station).count()
        return render(request, 'station/index.html', {'total_quotation': total_quotation})
