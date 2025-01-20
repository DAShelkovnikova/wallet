from django.db import models
from django.db import transaction


class Wallet(models.Model):
    """Модель Кошелька с полями
    uuid - поле типа UUIDField, которое используется в качестве первичного ключа.
    Оно автоматически заполняется уникальным значением при создании нового объекта Wallet
    balance - поле типа DecimalField, которое хранит баланс кошелька. Оно может содержать до 10 цифр,
    из которых 2 — после запятой. Значение по умолчанию — 0.00."""
    uuid = models.UUIDField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def deposit(self, amount):
        """Функция внесения суммы на счет кошелька.transaction.atomic(), чтобы гарантировать,
        что все операции внутри блока будут выполнены как единое целое. Если что-то пойдет не так,
        все изменения будут отменены. Баланс увеличивается на указанную сумму, и затем изменения сохраняются в базе
        данных с помощью self.save()."""
        with transaction.atomic():
            self.balance += amount
            self.save()


    def withdraw(self, amount):
        """Функция снятия суммы со счета кошелька. Сначала проверяется, достаточно ли средств на счете.
        Если запрашиваемая сумма больше текущего баланса, выбрасывается исключение ValueError с сообщением
        "Недостаточно средств". Если средств достаточно, снова используется transaction.atomic(),
        чтобы обеспечить целостность операции. Баланс уменьшается на указанную сумму, и изменения сохраняются в
        базе данных."""
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        with transaction.atomic():
            self.balance -= amount
            self.save()



