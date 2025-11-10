from django.urls import path
from .views import balance_view, balances_batch_view, top_holders_view

urlpatterns = [
    path("balance/<str:address>/", balance_view, name="balance"),
    path("balances/", balances_batch_view, name="balances_batch"),
    path("top/<int:top_n>/", top_holders_view, name="top_holders"),
]