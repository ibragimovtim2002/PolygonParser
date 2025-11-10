from django.urls import path
from .views import balance_view, balances_batch_view

urlpatterns = [
    path("balance/<str:address>/", balance_view, name="balance"),
    path("balances/", balances_batch_view, name="balances_batch"),
]