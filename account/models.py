from django.db import models
import uuid
from shortuuid import ShortUUID
from shortuuid.django_fields import ShortUUIDField
from django_countries.fields import CountryField

# from shortuuid.django_fields import ShortUUIDField
from djmoney.models.fields import MoneyField
from smart_selects.db_fields import ChainedForeignKey
import account
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
IDENTITY_TYPE = (
    ("ID", "IDENTITY CARD"),
    ("LICENSE", "DRIVERS LICENSE"),
)

TRANSACTION_TYPE = (
    ("transfer", "TRANSFER"),
    ("received", "RECEIVED"),
    ("withdraw", "WITHDRAW"),
    ("refund", "REFUND"),
    ("request", "REQUEST"),
    ("none", "NONE"),
)

TRANSACTION_STATUS = (
    ("failed", "FAILED"),
    ("completed", "COMPLETED"),
    ("pending", "PENDING"),
    ("processing", "PROCESSING"),
    ("request_sent", "REQUEST SENT"),
    ("request_processing", "REQUEST PROCESSING"),
    ("request_completed", "REQUEST COMPLETED"),
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


class KYC(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    account = models.OneToOneField(
        Account, blank=True, null=True, on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="kyc_images",
    )
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS)
    gender = models.CharField(max_length=30, choices=GENDER)
    identity_type = models.CharField(max_length=100, choices=IDENTITY_TYPE)
    identity_image = models.ImageField(
        upload_to="kyc_images/identity", null=True, blank=True
    )

    dob = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc_signature")

    # address
    country = models.ForeignKey(
        "cities_light.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    city = ChainedForeignKey(
        "cities_light.City",
        chained_field="country",
        chained_model_field="country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=1000, blank=True, null=True)

    # contact information
    mobile = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    def full_address(self):
        return f"{self.address}, {self.city}, {self.country}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction_id = ShortUUIDField(
        unique=True, length=15, max_length=20, prefix="TRN", alphabet="1234567890"
    )
    amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
    )
    receiver = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="receiver_account"
    )
    sender = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="sender_account"
    )
    status = models.CharField(
        choices=TRANSACTION_STATUS, default="pending", max_length=30
    )
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE, default="none", max_length=30
    )
    transaction_description = models.CharField(
        max_length=1000, default="payment", blank=True, null=True
    )
    reference_number = ShortUUIDField(
        max_length=20, unique=True, length=15, alphabet="1234567890"
    )
    transaction_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_time_updated = models.DateTimeField(
        auto_now=False, blank=True, null=True
    )

    def __str__(self):
        try:
            return f"{self.sender.transaction.transaction_id}"
        except:
            return f"{self.transaction_id}"
