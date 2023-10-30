import time
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from account.models import KYC, Account, Transaction
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe


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

    if account.kyc_submitted == True:
        messages.success(request, "KYC submitted")
        return redirect("account")

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
            account.kyc_submitted = True

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
def account_view(request, account_number):
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


@login_required(login_url="loginUser")
def search_account(request):
    account = Account.objects.get(user=request.user)
    all_accounts = Account.objects.all()
    query = request.POST.get("search_query")
    previous_url = request.META.get("HTTP_REFERER", None)
    """
    if the account exists 
    Search the account for the query requested 
    """
    if query:
        all_accounts = all_accounts.filter(
            Q(account_number__icontains=query, status="active")
            | Q(account_id__icontains=query, status="active")
        ).distinct()
        if all_accounts.exists() == True:
            messages.success(request, "Accounts found")
        else:
            all_accounts = all_accounts.filter(status="active")

    kyc = KYC.objects.get(
        account=account,
    )

    context = {
        "account": account,
        "kyc": kyc,
        "all_accounts": all_accounts,
        "query": query,
        "previous_url": previous_url,
    }
    return render(request, "account/search-account.html", context)


@login_required(login_url="loginUser")
def transactions(request):
    account = Account.objects.get(user=request.user)

    context = {"account": account}
    return render(request, "account/transactions.html", context)


@login_required(login_url="loginUser")
def transfer_amount(request, account_number):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    available_amount = account.account_balance.amount
    previous_url = request.META.get("HTTP_REFERER", None)

    try:
        transfer_account = Account.objects.get(account_number=account_number)

    except Account.DoesNotExist:
        transfer_account = None
        messages.warning(request, "Account does not exist")

        return redirect("search_account")
    context = {
        "account": account,
        "kyc": kyc,
        "transfer_account": transfer_account,
        "previous_url": previous_url,
    }
    return render(request, "account/transfer_amount.html", context)


@login_required(login_url="loginUser")
def amount_transfer_process(request, account_number):
    print(account_number)
    account = request.user.account
    """
    getting the sender and receiver account information
    """
    transfer_account = Account.objects.get(account_number=account_number)
    print(transfer_account)

    if request.method == "POST":
        amount = float(request.POST.get("new-value"))
        description = request.POST.get("description")

        if (
            account.account_balance.amount > 0
            and account.account_balance.amount > amount
        ):
            print("processing transfer..")
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_description=description,
                receiver=transfer_account,
                sender=account,
                transaction_type="transfer",
                status="processing",
            )
            new_transaction.save()

            context = {"account": account, "transfer_account": transfer_account}
            messages.success(request, "processing payment")
            return redirect(
                "transaction_confirmation",
                account_number,
                new_transaction.transaction_id,
            )
        else:
            messages.warning(request, "Insufficient funds")
            return redirect("transfer_amount", account_number)
    else:
        messages.warning(request, "Something went wrong")
        return redirect("transfer_amount", transfer_account.account_number)


@login_required(login_url="loginUser")
def transaction_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    # print(account)
    transferred_account = Account.objects.get(account_number=account_number)
    # print(transferred_account)
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        # print(f"Transaction.objects.get(transaction_id={transaction_id})")
        # print("<-------------------------------->")
        # print(f"{Transaction.objects.get(transaction_id=transaction_id)}")

        # transaction_info = Transaction.objects.get(transaction_id=transaction_id)
    except ObjectDoesNotExist:
        messages.warning(request, "Transaction not found")
        redirect("search_account")
    context = {
        "account": account,
        "transferred_account": transferred_account,
        "kyc": kyc,
        "transaction": transaction,
    }
    return render(request, "account/payment-confirmation.html", context)


def transaction_process(request, account_number, transaction_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    # print(account)
    transferred_account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    pin = ""
    completed = False
    if request.method == "POST":
        pin_ = request.POST.get("pin1")

        for i in range(1, 5):
            pin_ = request.POST.get(f"pin{i}")
            pin += pin_

        if pin == account.pin:
            print(transaction.amount.amount)
            transaction.status = "completed"
            transaction.save()

            # deduction from senders account
            account.account_balance -= transaction.amount
            print(account.account_balance)
            account.save()

            # allocating the money to the receiver

            transferred_account.account_balance += transaction.amount
            transferred_account.save()
            messages.success(request, "Transaction successfully")
            return HttpResponse(status=204)
            # return redirect("transaction_confirmation", account_number, transaction_id)

        else:
            messages.success(request, "Pin is not correct please retry")
            return redirect("transaction_confirmation", account_number, transaction_id)
    else:
        messages.success(request, "Pin is not correct please retry")
        return redirect("transaction_confirmation", account_number, transaction_id)


def successful_transaction_confirmation(request, transaction_id):
    account = request.user.account
    kyc = account.kyc
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {"account": account, "kyc": kyc, "transaction": transaction}
    return render(request, "account/success.html", context)
