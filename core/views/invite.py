import json
from typing import Dict, Union

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from core.models.accounts import User
from station.models import ServiceStation
from supplier.models import SupplierAccount
from utils.base import BaseViewSet, Addon, BaseView
from core.tasks import email_notification


@method_decorator(login_required, name='dispatch')
class InviteView(BaseView, Addon):
    def get(self, request, *args, **kwargs):
        return render(request, 'invitation/index.html', {'type': kwargs.get('type')})

    def post(self, request, *args, **kwargs):
        context = {'status': 200}
        try:
            data = json.loads(request.body.decode('utf-8'))
            company = self.get_user_company()
            if data.get('type') == 'supplier':
                return self.process_supplier(data)
            elif data.get('type') == 'stations':
                return self.process_station(data)
            else:
                raise Exception('Invalid selection')
        except Exception as ex:
            context.update({'status': 400, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)

    def process_supplier(self, data):
        context = {'status': 200, 'url': '/administrator/suppliers/'}
        try:
            if User.objects.filter(email=data.get('email')).exists():
                raise Exception('Invite could not be sent because email already exist on the system')
            if SupplierAccount.objects.filter(company=self.get_user_company(), email=data.get('email')).exists():
                raise Exception('You have already invited this supplier,Kindly use resend invitation button')
            instance = SupplierAccount()
            instance.email = data.get('email')
            instance.name = data.get('name')
            instance.company = self.get_user_company()
            instance.invite_id = self.unique_alpha_numeric_generator(SupplierAccount, 'invite_id', 50)
            instance.save()
            subject = 'Supplier invitation'
            content = {
                'url': f'/invitation/supplier/{instance.invite_id}',
            }
            template = 'emails/invite.html'
            resp = email_notification(data.get('email'), subject, template, content)
            if resp.get('code') == 200:
                context.update({'message': 'Invite sent successfully'})
            else:
                instance.delete()
                raise Exception('Invite link could not be sent,Kindly try again')
        except Exception as ex:
            context.update({'status': 400, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)

    def process_station(self, data):
        context = {'status': 200, 'url': '/administrator/service-stations/'}
        try:
            if User.objects.filter(email=data.get('email')).exists():
                raise Exception('Invite could not be sent because email already exist on the system')
            if ServiceStation.objects.filter(company=self.get_user_company(), email=data.get('email')).exists():
                raise Exception('You have already invited this service station,Kindly use resend invitation button')
            instance = ServiceStation()
            instance.email = data.get('email')
            instance.name = data.get('name')
            instance.company = self.get_user_company()
            instance.invite_id = self.unique_alpha_numeric_generator(ServiceStation, 'invite_id', 50)
            instance.save()
            subject = 'Service station invitation'
            content = {
                'url': f'/invitation/station/{instance.invite_id}',
            }
            template = 'emails/invite.html'
            resp = email_notification(data.get('email'), subject, template, content)
            if resp.get('code') == 200:
                context.update({'message': 'Invite sent successfully'})
            else:
                instance.delete()
                raise Exception('Invite link could not be sent,Kindly try again')
        except Exception as ex:
            context.update({'status': 400, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)

    def delete(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        try:
            data = self.get_data(request)
            if bool(data.get('id')) is False:
                raise Exception('Invalid information supplied')
            if bool(data.get('type')) is False:
                raise Exception('Invalid user type supplied')
            if data.get('type') not in ['supplier', 'station']:
                raise Exception('Invalid user type supplied')
            if data.get('type') == 'supplier':
                if not SupplierAccount.objects.filter(id=data.get('id'),
                                                      company=self.get_user_company()).exists():
                    raise Exception('Supplier account does not exists')
                instance = SupplierAccount.objects.filter(id=data.get('id'),
                                                          company=self.get_user_company()).first()
                instance.delete()
            elif data.get('type') == 'station':
                if not ServiceStation.objects.filter(id=data.get('id'), company=self.get_user_company()).exists():
                    raise Exception('Station account does not exists')
                instance = ServiceStation.objects.filter(id=data.get('id'),
                                                         company=self.get_user_company()).first()
                instance.delete()
            else:
                raise Exception('Invalid user type supplied')
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)


def test(request):
    return render(request, 'email/supplier.html', locals())
