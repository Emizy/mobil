import json
from datetime import datetime, timedelta

import pytz
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status

from core.models.accounts import User
from station.models import ServiceStation
from supplier.models import SupplierAccount
from utils.base import Addon, BaseView
from core.tasks import email_notification

from django.contrib.auth import authenticate, logout, login


class LoginView(BaseView):
    @staticmethod
    def get(request):
        try:
            logout(request)
        except:
            pass
        return render(request, 'auth/login.html', locals())

    def post(self, request):
        context = {'status': 200}
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username').strip()
            password = data.get('password').strip()
            for key, value in data.items():
                if key not in ['username', 'password']:
                    raise Exception('Invalid parameter {}'.format(key))
            user = authenticate(request, username=username,
                                password=password)
            if user:
                login(request, user)
                if request.user.type == 0:
                    url = '/administrator/dashboard'
                elif request.user.type == 1:  # service station
                    url = '/supplier/dashboard'
                elif request.user.type == 2:  # supplier
                    url = '/station/dashboard'
                else:
                    url = '/main'
                context['url'] = url
                content = {'ip': '',
                           'browser_name': request.headers.get('User-Agent'),
                           'browser_version': '',
                           'device_name': request.headers.get('Sec-Ch-Ua-Platform'),
                           'location': '',
                           'isp': '',
                           'date': datetime.now(),
                           'name': user.first_name}
                template = 'emails/login_notification.html'
                email_notification.delay(user.email, '11PLC: Login notification', template, content)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = 'Invalid credentials,Kindly supply valid credentials'
        except Exception as ex:
            print(ex)
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)


class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
        except:
            pass
        return redirect('/login')


class AccessInvitationView(BaseView, Addon):
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        type = kwargs.get('type')
        context = {'status': 'error'}
        try:
            if type not in ['stations', 'supplier']:
                raise Exception('System could not validate your request,Kindly click the right link sent to your email')
            if type == 'supplier':
                supplier = SupplierAccount.objects.filter(invite_id=token)
                if not supplier:
                    raise Exception(
                        'System could not validate your request,Kindly click the right link sent to your email')
                if supplier.first().is_accepted is True:
                    raise Exception('This invite link has already expired')
                context.update(
                    {'status': 'success', 'email': supplier.first().email, 'type': 'supplier', 'token': token,
                     'role': 'Supplier'})
            else:
                station = ServiceStation.objects.filter(invite_id=token)
                if not station:
                    raise Exception(
                        'System could not validate your request,Kindly click the right link sent to your email')
                if station.first().is_accepted is True:
                    raise Exception('This invite link has already expired')
                context.update(
                    {'status': 'success', 'email': station.first().email, 'type': 'stations', 'token': token,
                     'role': 'Service station'})
        except Exception as ex:
            context.update({'message': str(ex), 'status': 'error'})
        return render(request, 'auth/access_invitation.html', context)

    def post(self, request, *args, **kwargs):
        context = {'status': status.HTTP_400_BAD_REQUEST}
        try:
            data = json.loads(request.body.decode('utf-8'))
            allow_type = ['stations', 'supplier']
            if data.get('type') not in allow_type:
                raise Exception('Kindly click the right link sent to your mail')
            if data.get('type') == 'supplier':
                return self.process_supplier(data)
            elif data.get('type') == 'stations':
                return self.process_station(data)
            else:
                raise Exception('We could not process this information due to missing parameter')
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return JsonResponse(context, status=context['status'])

    def process_supplier(self, data):
        context = {'status': status.HTTP_200_OK}
        try:
            if not SupplierAccount.objects.filter(invite_id=data.get('token')).exists():
                raise Exception('Your account creation could not be completed')
            instance = SupplierAccount.objects.filter(invite_id=data.get('token')).first()
            if bool(data.get('password')) is False:
                raise Exception('Kindly supply valid password for your account')
            user = User(
                email=instance.email,
                is_confirmed=True,
                username=self.unique_alpha_numeric_generator(SupplierAccount, 'invite_id', 50),
                type=1,
            )
            user.set_password(data.get('password'))
            user.save()
            instance.user = user
            instance.is_accepted = True
            instance.address = data.get('address')
            instance.invite_id = ''
            instance.save()
            context.update({'message': 'Account created successfully'})

        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)

    def process_station(self, data):
        context = {'status': status.HTTP_200_OK}
        try:
            if not ServiceStation.objects.filter(invite_id=data.get('token')).exists():
                raise Exception('Your account creation could not be completed')
            instance = ServiceStation.objects.filter(invite_id=data.get('token')).first()
            if bool(data.get('password')) is False:
                raise Exception('Kindly supply valid password for your account')
            user = User(
                email=instance.email,
                is_confirmed=True,
                username=self.unique_alpha_numeric_generator(SupplierAccount, 'invite_id', 50),
                type=2,
            )
            user.set_password(data.get('password'))
            user.save()
            instance.user = user
            instance.is_accepted = True
            instance.invite_id = ''
            instance.address = data.get('address')
            instance.save()
            context.update({'message': 'Account created successfully'})
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return JsonResponse(context, status=context['status'], safe=False)
