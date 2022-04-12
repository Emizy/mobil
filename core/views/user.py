from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from core.models import User
from core.serializers import InviteSerializer, UserSerializer
from supplier.models import SupplierAccount
from utils.base import BaseViewSet, Addon
from core.tasks import email_notification


class UserViewSet(BaseViewSet, Addon):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(
        operation_description="",
        responses={},
        operation_summary=""
    )
    def update(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        user_fields = ['email', 'first_name', 'last_name', 'mobile']
        try:
            data = self.get_data(request)
            instance = self.get_object()
            for field in user_fields:
                if field in data:
                    if bool(data.get(field)):
                        instance.__setattr__(field, data.get(field))
            instance.save()
            context.update({'status': status.HTTP_200_OK, 'data': self.serializer_class(instance).data})
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})

        return Response(context, status=context['status'])
