import uuid

import pytz
from django.db import models

from station.models import ServiceStation
from supplier.models import SupplierAccount, Branch
from utils.enums import QuotationStatus
from core.models.accounts import User

tz = pytz.timezone('Africa/Lagos')


class SupplierQuotations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField(default=0.0)
    file = models.FileField(upload_to='supplier/')
    status = models.CharField(max_length=255, choices=QuotationStatus.choices(), default=QuotationStatus.PENDING)
    notify_on_station_upload = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier_quotation'
        verbose_name = 'SupplierQuotation'
        verbose_name_plural = 'Supplier Quotations'

    def dumps(self):
        return {
            'id': self.id,
            'supplier': self.branch.name if self.branch else self.supplier_name,
            'invoice_date': self.invoice_date,
            'due_date': self.due_date,
            'invoice_number': self.invoice_number,
            'amount': self.amount,
            'status': self.status,
            'station': self.get_stations_status,
            'created_at': self.created_at.astimezone(tz).strftime("%d %B, %Y"),
            'updated_at': self.updated_at,
            'created_by': self.get_created_by_name if self.created_by else '',
        }

    def admin_dump(self):
        return {
            'id': self.id,
            'supplier': self.branch.supplier.name if self.branch else self.supplier_name,
            'invoice_date': self.invoice_date,
            'due_date': self.due_date,
            'invoice_number': self.invoice_number,
            'amount': self.amount,
            'status': self.status,
            'station': self.get_stations_status,
            'station_name': self.get_stations_name,
            'created_at': self.created_at.astimezone(tz).strftime("%d %B, %Y"),
            'updated_at': self.updated_at,
            'created_by': self.get_created_by_name if self.created_by else '',
        }

    @property
    def get_stations_status(self):
        if StationQuotations.objects.filter(invoice_number=self.invoice_number).exists():
            return True
        else:
            return False

    @property
    def get_stations_name(self):
        if StationQuotations.objects.filter(invoice_number=self.invoice_number).exists():
            name = StationQuotations.objects.filter(invoice_number=self.invoice_number).first()
            return name.station.name
        else:
            return '---'

    @property
    def get_created_by_name(self):
        if self.created_by.type == 1:
            return SupplierAccount.objects.filter(user=self.created_by).first().name
        else:
            return ''


class StationQuotations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station = models.ForeignKey(ServiceStation, on_delete=models.SET_NULL, null=True, blank=True)
    station_name = models.CharField(max_length=255, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField(default=0.0)
    file = models.FileField(upload_to='station/')
    status = models.CharField(max_length=255, choices=QuotationStatus.choices(), default=QuotationStatus.PENDING)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'station_quotation'
        verbose_name = 'StationQuotation'
        verbose_name_plural = 'Station Quotations'

    def dumps(self):
        return {
            'id': self.id,
            'station': self.station.name if self.station else self.station_name,
            'invoice_date': self.invoice_date,
            'due_date': self.due_date,
            'invoice_number': self.invoice_number,
            'amount': self.amount,
            'status': self.status,
            'supplier': self.get_supplier_status(),
            'created_at': self.created_at.astimezone(tz).strftime("%d %B, %Y"),
            'updated_at': self.updated_at,
            'created_by': self.get_created_by_name if self.created_by else '',
        }

    def get_supplier_status(self):
        if SupplierQuotations.objects.filter(invoice_number=self.invoice_number).exists():
            return True
        else:
            return False

    @property
    def get_created_by_name(self):
        if self.created_by.type == 2:
            return ServiceStation.objects.filter(user=self.created_by).first().name
        else:
            return ''
