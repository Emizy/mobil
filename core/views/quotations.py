from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required

from station.models import ServiceStation
from supplier.models import SupplierAccount
from core.models.quotations import StationQuotations, SupplierQuotations
from utils.base import BaseView
from utils.pagination import paginate


@method_decorator(login_required, name='dispatch')
class QuotationView(BaseView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('type') == 'supplier':
            return render(request, 'main/supplier-quotation.html', {})
        else:
            return render(request, 'main/stations.html', {})

    def post(self, request, *args, **kwargs):
        if kwargs.get('type') == 'supplier':
            return self.supplier_table(request)

    def supplier_table(self, request):
        get_report = request.POST.dict()
        length = int(request.POST.get('length', 10))
        start = int(request.POST.get('start'))
        page = start / length + 1
        if get_report['order[0][dir]'] == 'asc':
            direc = ''
        else:
            direc = '-'
        objs = SupplierQuotations.objects.all()
        if get_report.get('status'):
            objs = objs.filter(status=get_report.get('status'))
        if get_report['search[value]']:
            objs = objs.filter(
                Q(branch__name__icontains=get_report['search[value]']) |
                Q(branch__supplier__name__icontains=get_report['search[value]']) |
                Q(invoice_number__icontains=get_report['search[value]']) |
                Q(due_date__icontains=get_report['search[value]']) |
                Q(invoice_date__icontains=get_report['search[value]'])).order_by(
                '-pk')

        else:
            objs = objs.order_by(
                '-pk')
        if 'columns[6][search][value]' in get_report:
            if get_report['columns[6][search][value]']:
                objs = objs.filter(status=get_report['columns[6][search][value]'])
        if 'columns[3][search][value]' in get_report:
            try:
                splitter = get_report['columns[3][search][value]'].split('/')
                objs = objs.filter(invoice_date__gte=datetime.strptime(splitter[0], '%Y-%m-%d'),
                                   invoice_date__lte=datetime.strptime(splitter[1], '%Y-%m-%d')).order_by(
                    '-pk')
            except Exception as ex:
                objs = objs
        if 'columns[4][search][value]' in get_report:
            try:
                splitter = get_report['columns[4][search][value]'].split('/')
                objs = objs.filter(due_date__gte=datetime.strptime(splitter[0], '%Y-%m-%d'),
                                   due_date__lte=datetime.strptime(splitter[1], '%Y-%m-%d')).order_by(
                    '-pk')
            except Exception as ex:
                objs = objs

        obj_list = paginate(obj=objs, length=length, page=page)
        reports = [rep.admin_dump() for rep in obj_list]
        total_report = objs.count()
        data = {
            'draw': int(request.POST.get('draw')),
            'recordsTotal': total_report,
            'recordsFiltered': total_report,
            'data': reports
        }
        return JsonResponse(data, status=200, safe=False)


@method_decorator(login_required, name='dispatch')
class QuotationDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('type') == 'supplier':
            supplier_quote = SupplierQuotations.objects.filter(id=kwargs.get('id')).first()
            station_quote = StationQuotations.objects.filter(invoice_number=supplier_quote.invoice_number).first()
            return render(request, 'main/supplier-quotation-detail.html',
                          {'id': kwargs.get('id'), 'supplier_quote': supplier_quote, 'station_quote': station_quote})
        else:
            return render(request, 'main/stations.html', {})

    def post(self, request, *args, **kwargs):
        context = {'status': 400}
        try:
            invoice_number = request.POST.get('invoice_number')
            quotation_status = request.POST.get('status')
            if not SupplierQuotations.objects.filter(invoice_number=invoice_number).exists():
                raise Exception('Supplier is yet to upload their quotation copy')
            if not StationQuotations.objects.filter(invoice_number=invoice_number).exists():
                raise Exception('Station is yet to upload their quotation copy')
            supplier = SupplierQuotations.objects.filter(invoice_number=invoice_number).first()
            station_copy = StationQuotations.objects.filter(invoice_number=invoice_number).first()
            supplier.status = quotation_status
            supplier.save()
            station_copy.status = quotation_status
            station_copy.save()
            context.update({'status': 200, 'message': 'Quotation status changed successfully'})
        except Exception as ex:
            context.update({'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)


@method_decorator(login_required, name='dispatch')
class QuotationDetailCopy(BaseView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('type') == 'supplier':
            supplier_quote = SupplierQuotations.objects.filter(id=request.GET.get('id')).first()
            return JsonResponse(
                {'template': render_to_string('main/include/supplier-copy.html', {'supplier_quote': supplier_quote})},
                status=200, safe=False)
        elif request.GET.get('type') == 'station':
            supplier_quote = SupplierQuotations.objects.filter(id=request.GET.get('id')).first()
            station_quote = StationQuotations.objects.filter(invoice_number=supplier_quote.invoice_number).first()
            return JsonResponse(
                {'template': render_to_string('main/include/station-copy.html', {'station_quote': station_quote})},
                status=200, safe=False)
