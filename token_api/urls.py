from django.urls import path
from .views import balance_view, balances_batch_view, top_holders_view, top_holders_with_tx_view, token_info_view

urlpatterns = [
    path("balance/<str:address>/", balance_view, name="balance"),
    path("balances/", balances_batch_view, name="balances_batch"),
    path("top/<int:top_n>/", top_holders_view, name="top_holders"),
    path("top_with_tx/<int:top_n>/", top_holders_with_tx_view, name="top_holders_with_tx"),
    path("getinfo/token/<str:token_address>/", token_info_view, name="token_info"),
]