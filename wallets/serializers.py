from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        """Класс создает сериализатор для модели Wallet.
        В классе Meta указывается, что этот сериализатор связан с моделью Wallet.
        fields указывает какие поля модели будут включены в сериализацию"""
        model = Wallet
        fields = ['uuid', 'balance']


class OperationSerializer(serializers.Serializer):
    """Класс предназначен для сериализации данных, связанных с операциями над кошельком.
    operationType - поле для указания вид операции (DEPOSIT или WITHDRAW). Это поле будет проверять, что введенное
    значение соответствует одному из указанных вариантов.
    amount - поле, которое представляет собой десятичное число. max_digits=10: Максимальное количество цифр,
    включая цифры до и после десятичной точки. decimal_places=2: Количество цифр после десятичной точки,
    что позволяет хранить суммы с двумя знаками после запятой."""
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
