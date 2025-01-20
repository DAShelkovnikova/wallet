from django.test import TestCase
from .models import Wallet
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class WalletTests(TestCase):
    def setUp(self):
        """Метод выполняется перед каждым тестом.
        Создается кошелек с UUID и начальным балансом 1000.0
        Инициализируется экземпляр APIClient, который будет использоваться для тестирования API."""
        self.wallet = Wallet.objects.create(uuid='123e4567-e89b-12d3-a456-426614174000', balance=1000.00)
        self.client = APIClient()


    def test_deposit(self):
        """Тест пополнения кошелька"""
        self.wallet.deposit(500)
        self.assertEqual(self.wallet.balance, 1500.00)


    def test_withdraw(self):
        """Тест на снятие денег с кошелька"""
        self.wallet.withdraw(500)
        self.assertEqual(self.wallet.balance, 500.00)


    def test_withdraw_insufficient_funds(self):
        """Тест на работу исключения, при недостатке средств на счете"""
        with self.assertRaises(ValueError):
            self.wallet.withdraw(2000)


    def test_wallet_balance(self):
        """Тест начального баланса"""
        self.assertEqual(self.wallet.balance, 1000.00)


    def test_successful_deposit_api(self):
        """Тест пополнения кошелька через API"""
        response = self.client.post(reverse('wallet-operation', args=[self.wallet.uuid]),
                                    {'operationType': 'DEPOSIT', 'amount': 500},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1500.00)


    def test_successful_withdraw_api(self):
        """Тест снятия денег с кошелька через API"""
        response = self.client.post(reverse('wallet-operation', args=[self.wallet.uuid]),
                                    {'operationType': 'WITHDRAW', 'amount': 500},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 500.00)


    def test_withdraw_insufficient_funds_api(self):
        """Тест на работу исключения, при недостатке средств на счете через API"""
        response = self.client.post(reverse('wallet-operation', args=[self.wallet.uuid]),
                                    {'operationType': 'WITHDRAW', 'amount': 2000},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


    def test_invalid_json_api(self):
        """Тест на неверный формат JSON в запросе"""
        response = self.client.post(reverse('wallet-operation', args=[self.wallet.uuid]),
                                    {'operationType': 'DEPOSIT'},  # amount отсутствует
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


