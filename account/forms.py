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
from .models import KYC


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
