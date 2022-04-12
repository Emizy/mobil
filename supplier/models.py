import pytz
from django.db import models

from core.abstract.abstracts import UserRel
from core.models.accounts import AuthToken, Company

tz = pytz.timezone('Africa/Lagos')


class SupplierAccount(UserRel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    invite_id = models.CharField(max_length=255, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'
        ordering = ('-created_at',)

    def __str__(self):
        return self.email


class Branch(models.Model):
    supplier = models.ForeignKey(SupplierAccount, on_delete=models.CASCADE, related_name='supplier_branch')
    name = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(default='')
    phone = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'branch'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def dump_(self):
        return {
            'name': self.name,
            'state': self.state,
            'status': self.get_manager_status,
            'manager_name': self.get_manager_name,
            'id': self.id,
            'phone': self.phone,
            'created_at': self.created_at.astimezone(tz).strftime("%d %B, %Y")
        }

    @property
    def get_manager_name(self):
        if SupplierEmployee.objects.filter(branch_id=self.id).exists():
            return SupplierEmployee.objects.filter(branch_id=self.id).first().name
        else:
            return '---'

    @property
    def get_manager_status(self):
        if SupplierEmployee.objects.filter(branch_id=self.id).exists():
            status = SupplierEmployee.objects.filter(branch_id=self.id).first()
            if status.status is True:
                return 'ACCEPTED'
            else:
                return 'PENDING'
        else:
            return 'PENDING'


class SupplierEmployee(UserRel):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, related_name='branch_users', null=True, blank=True)
    invite_code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier_employee'
        ordering = ('-created_at',)

    def __str__(self):
        return self.email
