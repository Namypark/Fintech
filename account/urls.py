from . import views
from django.urls import path

urlpatterns = [
    path("kyc-registration/", views.kyc_registration, name="kyc-registration"),
    path("account/<account_number>", views.account_view, name="account"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("search-account/", views.search_account, name="search_account"),
    path(
        "transfer_amount/<int:account_number>",
        views.transfer_amount,
        name="transfer_amount",
    ),
    path("transactions/", views.transactions, name="transactions"),
    path(
        "amount-transfer-process/<int:account_number>",
        views.amount_transfer_process,
        name="amount_transfer_process",
    ),
    path(
        "transfer-confirmation/<int:account_number>/<str:transaction_id>",
        views.transaction_confirmation,
        name="transaction_confirmation",
    ),
    path(
        "transaction_process/<int:account_number>/<str:transaction_id>",
        views.transaction_process,
        name="transaction_process",
    ),
    path(
        "successful_transaction_confirmation/<str:transaction_id>",
        views.successful_transaction_confirmation,
        name="transaction_confirmation",
    ),
    path(
        "transaction_detail/<str:transaction_id>",
        views.transaction_detail,
        name="transaction_detail",
    ),
]
