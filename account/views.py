from django.shortcuts import redirect, render
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="loginUser")
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)
    try:
        """
        get the KYC
        """
        kyc = KYC.objects.get(user=user)

    except KYC.DoesNotExist:
        kyc = None

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        # print("posted -----------")
        # print(request.POST.get("full_name"))
        # print(request.POST.get("gender"))
        # print(request.POST.get("mobile"))
        # print(request.POST.get("marital_status"))
        # print(request.POST.get("identity_type"))
        # print(request.POST.get("country"))
        # print(request.POST.get("city"))
        # print(request.POST.get("dob"))
        # print(request.POST.get("address"))
        # print(request.POST.get("image"))
        # print(request.POST.get("identity_image"))
        # print(request.POST.get("signature"))

        if form.is_valid():
            print("form is valid")
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC form submitted successfully.")
            messages.success(request, "KYC form is being reviewed.")

            return redirect("home")
        else:
            print("form is invalid")
            print(form.errors)
            form = KYCForm(instance=kyc)
    else:
        form = KYCForm(instance=kyc)

    context = {"form": form, "account": account, "kyc": kyc}

    return render(request, "account/kyc-form.html", context)


@login_required(login_url="loginUser")
def account_view(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        kyc = None
        messages.warning(
            request, "Please you must submit kyc documents before viewing this "
        )
        return redirect("kyc-registration")

    context = {"account": account, "kyc": kyc}
    return render(request, "account/account.html", context)


def test_view(request):
    form = KYCForm()

    context = {"form": form}
    return render(request, "account/test.html", context)
