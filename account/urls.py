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
        name="successful_transaction_confirmation",
    ),
    path(
        "transaction_detail/<str:transaction_id>",
        views.transaction_detail,
        name="transaction_detail",
    ),
    path(
        "receive_request/",
        views.receive_request,
        name="receive_request",
    ),
    path(
        "receive_request/<account_id>",
        views.receive_request_2,
        name="receive_request_2",
    ),
    path(
        "amount-request/<account_id>",
        views.request_process,
        name="request_process",
    ),
    path(
        "amount-request-confirmation/<str:transaction_id>",
        views.receive_request_3,
        name="receive_request_3",
    ),
    path(
        "receive_request_confirmation/<str:transaction_id>",
        views.receive_request_confirmation,
        name="receive_request_confirmation",
    ),
    path(
        "successful_request_confirmation/<str:transaction_id>",
        views.successful_request_confirmation,
        name="successful_request_confirmation",
    ),
    path(
        "successful_request_confirmation/<str:transaction_id>",
        views.successful_request_confirmation,
        name="successful_request_confirmation",
    ),
    path(
        "accept_request/<str:transaction_id>",
        views.accept_request,
        name="accept_request",
    ),
    path(
        "cancel_request/<str:transaction_id>",
        views.cancel_request,
        name="cancel_request",
    ),
    path(
        "decline_request/<str:transaction_id>",
        views.decline_request,
        name="decline_request",
    ),
    path(
        "request_transaction_detail/<str:transaction_id>",
        views.request_transaction_detail,
        name="request_transaction_detail",
    ),
]
