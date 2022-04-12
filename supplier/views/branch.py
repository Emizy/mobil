from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from core.models.quotations import SupplierQuotations
from utils.base import BaseView
from supplier.models import Branch, SupplierAccount, SupplierEmployee
from utils.pagination import paginate
from utils.country.countries import country_codes, Countries


@method_decorator(login_required, name='dispatch')
class BranchView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'supplier/branch.html', locals())

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
        objs = Branch.objects.filter(supplier=supplier)
        if get_report['search[value]']:
            objs = objs.filter(branch__supplier=supplier).filter(
                Q(name=get_report['search[value]']) |
                Q(state=get_report['search[value]'])).order_by(
                '-pk')
        obj_list = paginate(obj=objs, length=length, page=page)
        reports = [rep.dump_() for rep in obj_list]
        total_report = objs.count()
        data = {
            'draw': int(request.POST.get('draw')),
            'recordsTotal': total_report,
            'recordsFiltered': total_report,
            'data': reports
        }
        return JsonResponse(data, status=200, safe=False)


@method_decorator(login_required, name='dispatch')
class CreateBranchView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'supplier/create-branch.html',
                      {'states': self.states('234')})

    def post(self, request, *args, **kwargs):
        supplier = SupplierAccount.objects.filter(user=request.user).first()
        context = {'status': 400}
        try:
            if Branch.objects.filter(name=request.POST.get('name'), state=request.POST.get('state')).exists():
                raise Exception('Branch already exist')
            if SupplierEmployee.objects.filter(email=request.POST.get('manager_email')).exists():
                raise Exception('You can only invite a supplier to a single branch')
            branch_payload = {
                'name': request.POST.get('name'),
                'state': request.POST.get('state'),
                'address': request.POST.get('address'),
                'supplier': supplier
            }
            obj = Branch.objects.create(**branch_payload)
            # employee = {
            #     'name': request.POST.get('manager_name'),
            #     'email': request.POST.get('manager_email'),
            # }
            context.update({'status': 200, 'message': 'Branch created successfully'})
        except Exception as ex:
            context.update({'status': 400, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)

    @staticmethod
    def states(calling_code):
        country = dict(country_codes).get(calling_code).replace('({})'.format(calling_code), '').strip()
        country = Countries(country)
        return country.provinces()
