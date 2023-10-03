from sys import prefix
from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField

# from shortuuid.django_fields import ShortUUIDField
from djmoney.models.fields import MoneyField
from userAuth.models import User

# Create your models here.
ACCOUNT_STATUS = (
    ("active", "Active"),
    ("in_active", "Inactive"),
)

GENDER = (
    ("male", "MALE"),
    ("female", "FEMALE"),
    ("other", "OTHER"),
)

MARITAL_STATUS = (
    ("single", "SINGLE"),
    ("married", "MARRIED"),
    ("divorced", "DIVORCED"),
)


def user_directory_path(instance, path):
    ext: filename = path.split(".")[-1]
    filename = f"{instance.id}_{ext}"
    return f"user_{instance.user.id}/{filename}"


class Account(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    account_balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
    )
    account_id = ShortUUIDField(
        length=7, max_length=22, unique=True, prefix="NGN", alphabet="1234567890"
    )
    account_number = ShortUUIDField(
        length=10, max_length=22, unique=True, alphabet="1234567890", prefix="217"
    )
    pin = ShortUUIDField(length=4, max_length=7, alphabet="1234567890", editable=True)
    ref_code = ShortUUIDField(
        unique=True, length=7, max_length=22, alphabet="abcdefgh1234567890"
    )
    status = models.CharField(
        choices=ACCOUNT_STATUS, max_length=100, default="in_active"
    )
    date = models.DateField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    referred_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="referred_by",
    )

    class Meta:
        ordering: list[str] = ["-date"]

    def __str__(self) -> str:
        return f"{self.user}"

    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
