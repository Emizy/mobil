from django.db import models

from core.models.accounts import User


class UserRel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name="%(class)s",
        editable=True,
        null=True, blank=True
    )

    class Meta:
        abstract = True
