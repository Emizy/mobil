import uuid
from django.utils.crypto import get_random_string
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models.accounts import AuthToken, User, Company


class Addon:
    def __init__(self):
        super().__init__()

    @staticmethod
    def verify(payload):
        if User.objects.filter(**payload).exists():
            return True
        return False

    def generate_uuid(self, model, column):
        unique = str(uuid.uuid4())
        kwargs = {column: unique}
        qs_exists = model.objects.filter(**kwargs).exists()
        if qs_exists:
            return self.generate_uuid(model, column)
        return unique

    @staticmethod
    def create_auth_token(data):
        instance = AuthToken.objects.create(**data)
        return instance

    def unique_number_generator(self, model, field, length=6, allowed_chars="0123456789"):
        unique = get_random_string(length=length, allowed_chars=allowed_chars)
        kwargs = {field: unique}
        qs_exists = model.objects.filter(**kwargs).exists()
        if qs_exists:
            return self.unique_number_generator(model, field, length)
        return unique

    def unique_alpha_numeric_generator(self, model, field, length=6,
                                       allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        unique = get_random_string(length=length, allowed_chars=allowed_chars)
        kwargs = {field: unique}
        qs_exists = model.objects.filter(**kwargs).exists()
        if qs_exists:
            return self.unique_alpha_numeric_generator(model, field)
        return unique

    @staticmethod
    def delete_auth_token(data):
        try:
            AuthToken.objects.filter(**data).first().delete()
        except Exception as ex:
            pass

    @staticmethod
    def check_model_field_exist(model, data):
        if model.objects.filter(**data).exists():
            return True
        return False

    @staticmethod
    def get_model_field(model, data):
        return model.objects.filter(**data)


class CustomFilter(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.query_params, queryset=queryset, request=request).qs
        return queryset


class BaseViewSet(ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    """
    This class inherit from django ViewSet class
    """
    custom_filter_class = CustomFilter()
    search_backends = SearchFilter()
    order_backend = OrderingFilter()

    def get_list(self, queryset):
        if 'search' in self.request.query_params:
            query_set = self.search_backends.filter_queryset(request=self.request,
                                                             queryset=queryset,
                                                             view=self)
        elif self.request.query_params:
            query_set = self.custom_filter_class.filter_queryset(request=self.request,
                                                                 queryset=queryset,
                                                                 view=self)
        else:
            query_set = queryset
        if 'ordering' in self.request.query_params:
            query_set = self.order_backend.filter_queryset(query_set, self.request, self)
        else:
            query_set = query_set.order_by('pk')
        return query_set

    def paginator(self, queryset, serializer_class):
        paginated_data = self.paginator_class.generate_response(queryset, serializer_class, self.request)
        return paginated_data

    @staticmethod
    def get_data(request) -> dict:
        return request.data if isinstance(request.data, dict) else request.data.dict()

    def get_user_company(self):
        if Company.objects.filter(user=self.request.user).exists():
            return Company.objects.filter(user=self.request.user).first()
        else:
            raise Exception('No company attached to this user')


class BaseView(View):
    custom_filter_class = CustomFilter()
    search_backends = SearchFilter()
    order_backend = OrderingFilter()

    @staticmethod
    def get_data(request) -> dict:
        return request.data if isinstance(request.data, dict) else request.data.dict()

    def get_user_company(self):
        print(self.request.user)
        if Company.objects.filter(user=self.request.user).exists():
            return Company.objects.filter(user=self.request.user).first()
        else:
            raise Exception('No company attached to this user')


class BaseModelViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_data(request) -> dict:
        return request.data if isinstance(request.data, dict) else request.data.dict()
