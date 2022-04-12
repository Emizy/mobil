from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from core.tasks import email_notification
from core.models.quotations import StationQuotations, SupplierQuotations
from utils.base import BaseView
from station.models import ServiceStation
from utils.pagination import paginate


@method_decorator(login_required, name='dispatch')
class QuotationView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'station/quotation.html', locals())

    def post(self, request, *args, **kwargs):
        station = ServiceStation.objects.filter(user=request.user).first()
        get_report = request.POST.dict()
        length = int(request.POST.get('length', 10))
        start = int(request.POST.get('start'))
        page = start / length + 1
        if get_report['order[0][dir]'] == 'asc':
            direc = ''
        else:
            direc = '-'
        if get_report['search[value]']:
            objs = StationQuotations.objects.filter(station=station).filter(
                Q(invoice_number__icontain=get_report['search[value]']) |
                Q(due_date__icontain=get_report['search[value]']) |
                Q(invoice_date__icontain=get_report['search[value]'])).order_by(
                '-pk')
        else:
            objs = StationQuotations.objects.filter(station=station).order_by(
                '-pk')
        obj_list = paginate(obj=objs, length=length, page=page)
        reports = [rep.dumps() for rep in obj_list]
        total_report = objs.count()
        data = {
            'draw': int(request.POST.get('draw')),
            'recordsTotal': total_report,
            'recordsFiltered': total_report,
            'data': reports
        }
        return JsonResponse(data, status=200, safe=False)


@method_decorator(login_required, name='dispatch')
class CreateQuotation(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'station/create-quotation.html', {})

    def post(self, request, *args, **kwargs):
        context = {'status': 400}
        try:
            station = ServiceStation.objects.filter(user=request.user).first()
            if StationQuotations.objects.filter(invoice_number=request.POST.get('invoice_number'),
                                                station=station).exists():
                raise Exception(
                    f'Quotation with invoice number:{request.POST.get("invoice_number")} already exist')
            payload = {
                'due_date': request.POST.get('due_date'),
                'invoice_date': request.POST.get('invoice_date'),
                'invoice_number': request.POST.get('invoice_number'),
                'amount': request.POST.get('amount'),
                'station': station,
                'status': 'PENDING',
                'created_by': request.user,
            }
            obj = StationQuotations.objects.create(**payload)
            obj.file = request.FILES['file']
            obj.save()
            # send notification to supplier
            if SupplierQuotations.objects.filter(invoice_number=request.POST.get('invoice_number')).exists():
                instance = SupplierQuotations.objects.filter(invoice_number=request.POST.get('invoice_number')).first()
                message = {'email': instance.branch.supplier.email,
                           'message': f'We are glad to inform you that {station.name} '
                                      f'has just uploaded the receipt for invoice number: {request.POST.get("invoice_number")}'}
                email_notification(message.get('email'),
                                   f'RE: Invoice notification for {request.POST.get("invoice_number")}',
                                   'emails/station_reciept_upload', message)
            context.update({'status': 200, 'message': 'Quotation submitted successfully'})
        except Exception as ex:
            context.update({'status': 400, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)
