from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from core.models.quotations import SupplierQuotations
from utils.base import BaseView
from supplier.models import Branch, SupplierAccount
from utils.pagination import paginate


@method_decorator(login_required, name='dispatch')
class QuotationView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'supplier/quotations.html', locals())

    def post(self, request, *args, **kwargs):
        supplier = SupplierAccount.objects.filter(user=request.user).first()
        get_report = request.POST.dict()
        length = int(request.POST.get('length', 10))
        start = int(request.POST.get('start'))
        page = start / length + 1
        if get_report['order[0][dir]'] == 'asc':
            direc = ''
        else:
            direc = '-'
        if get_report['search[value]']:
            objs = SupplierQuotations.objects.filter(branch__supplier=supplier).filter(
                Q(branch__name=get_report['search[value]']) |
                Q(invoice_number__icontain=get_report['search[value]']) |
                Q(due_date__icontain=get_report['search[value]']) |
                Q(invoice_date__icontain=get_report['search[value]'])).order_by(
                '-pk')
        else:
            objs = SupplierQuotations.objects.filter(branch__supplier=supplier).order_by(
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
        branches = Branch.objects.all()
        return render(request, 'supplier/create-quotation.html', {'branches': branches})

    def post(self, request, *args, **kwargs):
        context = {'status': 400}
        try:
            if not Branch.objects.filter(id=request.POST.get('branch')).exists():
                raise Exception('Branch does not exist')
            branch = Branch.objects.filter(id=request.POST.get('branch')).first()
            if SupplierQuotations.objects.filter(branch=branch,
                                                 invoice_number=request.POST.get('invoice_number')).exists():
                raise Exception(
                    f'Quotation with invoice number:{request.POST.get("invoice_number")} already exist for this branch')
            payload = {
                'due_date': request.POST.get('due_date'),
                'invoice_date': request.POST.get('invoice_date'),
                'invoice_number': request.POST.get('invoice_number'),
                'amount': request.POST.get('amount'),
                'status': 'PENDING',
                'branch': branch,
                'created_by': request.user,
            }
            obj = SupplierQuotations.objects.create(**payload)
            obj.file = request.FILES['file']
            obj.save()
            context.update({'status': 200, 'message': 'Quotation submitted successfully'})
        except Exception as ex:
            context.update({'status': 400, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)
