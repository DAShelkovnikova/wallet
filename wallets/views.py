from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer


class WalletCreateView(APIView):

    def post(self, request):
        """Класс и функция для обработки POST запроса для создания нового кошелька.
        serializer = WalletSerializer(data=request.data): Создает экземпляр сериализатора с данными из запроса.
        if serializer.is_valid(): Проверяет, валидны ли данные.
        wallet = serializer.save(): Сохраняет новый кошелек в базе данных.
        return Response(...): Возвращает ответ с UUID и балансом нового кошелька и статусом 201 (создано).
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST):
        Если данные не валидны, возвращает ошибки с кодом 400."""
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet = serializer.save()
            return Response({"uuid": wallet.uuid, "balance": wallet.balance}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletOperationView(APIView):
    def post(self, request, WALLET_UUID):
        """Класс и функция для обработки POST запроса для проведения операций с кошельком.
        post(self, request, WALLET_UUID): Метод для обработки операций с кошельком (депозит или вывод).
        wallet = Wallet.objects.get(uuid=WALLET_UUID): Пытается получить кошелек по UUID. Если не находит,
        возвращает ошибку 404 (не найдено).
        serializer = OperationSerializer(data=request.data): Создает экземпляр сериализатора для операции.
        if serializer.is_valid(): Проверяет валидность данных операции.
        operation_type и amount: Извлекает тип операции и сумму из валидированных данных.
        if operation_type == 'DEPOSIT': Если операция — депозит, вызывает метод deposit у кошелька.
        elif operation_type == 'WITHDRAW': Если операция — вывод, вызывает метод withdraw.
        return Response(...): Возвращает текущий баланс после операции с кодом 200 (успешно).
        except ValueError as e: Обрабатывает ошибки, возникающие при выполнении операций, и возвращает их с кодом 400.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST): Если данные не валидны,
        возвращает ошибки."""
        try:
            wallet = Wallet.objects.get(uuid=WALLET_UUID)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            operation_type = serializer.validated_data['operationType']
            amount = serializer.validated_data['amount']

            try:
                if operation_type == 'DEPOSIT':
                    wallet.deposit(amount)
                elif operation_type == 'WITHDRAW':
                    wallet.withdraw(amount)
                return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletBalanceView(APIView):
    def get(self, request, WALLET_UUID):
        """get(self, request, WALLET_UUID): Метод для получения информации о балансе кошелька.
        wallet = Wallet.objects.get(uuid=WALLET_UUID): Пытается получить кошелек по UUID.
        Если не находит, возвращает ошибку 404.
        serializer = WalletSerializer(wallet): Сериализует данные кошелька.
        return Response(serializer.data, status=status.HTTP_200_OK): Возвращает данные о кошельке с кодом 200.
        except Wallet.DoesNotExist: Обрабатывает случай, когда кошелек не найден, и возвращает ошибку 404"""
        try:
            wallet = Wallet.objects.get(uuid=WALLET_UUID)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)



