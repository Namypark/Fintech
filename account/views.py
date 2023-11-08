from multiprocessing import context
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
        if all_accounts.exists():
            messages.success(request, "Accounts found")
        else:
            all_accounts = all_accounts.filter(status="active")

    kyc = account.kyc

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

    except:
        transfer_account = None

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


@login_required(login_url="loginUser")
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
            messages.success(request, "Transaction successful")
            time.sleep(3)
            return redirect(
                "successful_transaction_confirmation", transaction.transaction_id
            )

        else:
            messages.success(request, "Pin is not correct please retry")
            return redirect("transaction_confirmation", account_number, transaction_id)
    else:
        messages.success(request, "Pin is not correct please retry")
        return redirect("transaction_confirmation", account_number, transaction_id)


@login_required(login_url="loginUser")
def successful_transaction_confirmation(request, transaction_id):
    account = request.user.account
    kyc = account.kyc
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {"account": account, "kyc": kyc, "transaction": transaction}
    return render(request, "account/success.html", context)


@login_required(login_url="loginUser")
def dashboard(request):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    transaction = Transaction.objects.filter(user=request.user)
    sender_transaction = transaction.filter(sender=account).order_by(
        "-transaction_time"
    )
    receiver_transaction = Transaction.objects.filter(receiver=account).order_by(
        "-transaction_time"
    )

    context = {
        "account": account,
        "kyc": kyc,
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction,
        "transaction": transaction,
    }

    return render(request, "account/dashboard.html", context)


@login_required(login_url="loginUser")
def transaction_detail(request, transaction_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc

    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)

    except Transaction.DoesNotExist:
        transaction = None
        messages.warning(request, "Transaction does not exist")
        redirect("dashboard")
    context = {"transaction": transaction, "kyc": kyc}
    return render(request, "account/transaction_details.html", context)


@login_required(login_url="loginUser")
def receive_request(request):
    account = Account.objects.get(user=request.user)
    all_accounts = None
    kyc = account.kyc
    previous_url = request.META.get("HTTP_REFERER", None)
    query = request.POST.get("search_query")

    if query:
        all_accounts = Account.objects.filter(
            Q(account_number__icontains=query, status="active")
            | Q(account_id__icontains=query, status="active")
        ).distinct()

    context = {
        "kyc": kyc,
        "all_accounts": all_accounts,
        "previous_url": previous_url,
        "query": query,
        "account": account,
    }
    return render(request, "account/receive_payment.html", context)


def receive_request_2(request, account_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    requested_account = Account.objects.get(account_number=account_id)

    context = {"kyc": kyc, "requested_account": requested_account, "account": account}
    return render(request, "account/receive_payment2.html", context)


def request_process(request, account_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    requested_account = Account.objects.get(account_number=account_id)

    # print(requested_account)
    print("before post")
    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        transaction = Transaction.objects.create(
            user=request.user,
            amount=amount,
            status="request_processing",
            transaction_type="request",
            transaction_description=description,
            sender=account,
            receiver=requested_account,
        )
        transaction.save()
        print("save")
        return redirect("receive_request_3", transaction_id=transaction.transaction_id)
    else:
        messages.warning(
            request, "Error something went wrong with with the transaction"
        )
        return redirect("receive_request_2", account_id)


def receive_request_3(request, transaction_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    transaction.status = "request_sent"
    transaction.save()
    requested_account = transaction.receiver
    context = {
        "account": account,
        "kyc": kyc,
        "transaction": transaction,
        "requested_account": requested_account,
    }
    return render(request, "account/receive_payment3.html", context)


def receive_request_confirmation(request, transaction_id):
    account = Account.objects.get(user=request.user)
    kyc = account.kyc
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    pin = ""
    if request.method == "POST":
        pin_ = request.POST.get("pin1")

        for i in range(1, 5):
            pin_ = request.POST.get(f"pin{i}")
            pin += pin_

        if pin == account.pin:
            transaction.status = "request_completed"
            transaction.save()

            # deduction from senders account

            # allocating the money to the receiver
            messages.success(request, "Request successful")
            return redirect("successful_request_confirmation", transaction_id)

        else:
            messages.warning(request, "Pin is not correct please retry")
            return redirect("receive_request_3", transaction_id)
    else:
        return redirect("receive_request_3", transaction_id)


def successful_request_confirmation(request, transaction_id):
    account = request.user.account
    kyc = account.kyc
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {"account": account, "kyc": kyc, "transaction": transaction}
    return render(request, "account/request_success.html", context)
