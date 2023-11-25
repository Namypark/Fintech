from datetime import datetime
from django import forms
from django.forms import (
    ImageField,
    DateInput,
    FileInput,
    ModelForm,
    Select,
    TextInput,
    Widget,
)
from .models import KYC, CreditCard


class DateInput(DateInput):
    input_type = "date"


class KYCForm(ModelForm):
    identity_image = ImageField(widget=FileInput, required=True)
    image = ImageField(widget=FileInput, required=True)
    signature = ImageField(widget=FileInput, required=True)

    class Meta:
        model = KYC
        fields = [
            "full_name",
            "image",
            "marital_status",
            "gender",
            "identity_type",
            "identity_image",
            "dob",
            "signature",
            "country",
            "city",
            "mobile",
            "address",
        ]
        widgets = {
            "full_name": TextInput(
                attrs={
                    "placeholder": "Enter your full name",
                    "required": True,
                }
            ),
            "mobile": TextInput(
                attrs={
                    "placeholder": "Enter your mobile number",
                    "required": True,
                },
            ),
            "dob": DateInput,
            "full_name": TextInput(
                attrs={
                    "placeholder": "Enter your full name",
                    "required": True,
                }
            ),
        }


# data-value="16318" data-auto_choose="false"data-chainfield="country" data-url="/chaining/filter/cities_light/City/country/account/KYC/city" data-value="16318" data-auto_choose="false"


class CreditCardForm(ModelForm):
    cardholder_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your cardholder name", "required": True}
        )
    )
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your card number",
                "required": True,
            }
        ),
    )
    expiration_month = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "04",
                "required": True,
                "id": "expiration_month",
                "min": 1,
                "max": 12,
            }
        )
    )
    expiration_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "2025",
                "required": True,
                "id": "expiration_year",
                "min": datetime.today().year,
                "max": 9999,
            }
        )
    )
    cvv = forms.CharField(
        min_length=3,
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "placeholder": "112",
                "required": True,
                "id": "cvv",
            }
        ),
    )

    class Meta:
        model = CreditCard
        fields = [
            "cardholder_name",
            "card_number",
            "card_type",
            "expiration_month",
            "expiration_year",
            "cvv",
        ]
