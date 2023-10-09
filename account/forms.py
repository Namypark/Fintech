from sqlite3 import Date
from django.forms import ImageField, DateInput, FileInput, ModelForm, TextInput, Widget
from .models import KYC


class DateInput(DateInput):
    input_type = "date"


class KYCForm(ModelForm):
    identity_image = ImageField(
        widget=FileInput,
    )
    image = ImageField(widget=FileInput)

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
                }
            ),
            "mobile": TextInput(
                attrs={
                    "placeholder": "Enter your mobile number",
                },
            ),
            "dob": DateInput,
        }
