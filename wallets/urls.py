from django.urls import path
from .views import WalletOperationView, WalletBalanceView, WalletCreateView

urlpatterns = [
    path('api/v1/wallets/', WalletCreateView.as_view(), name='create-wallet'),
    path('api/v1/wallets/<uuid:WALLET_UUID>/operation', WalletOperationView.as_view(), name='wallet-operation'),
    path('api/v1/wallets/<uuid:WALLET_UUID>', WalletBalanceView.as_view(), name='wallet-balance'),
]
