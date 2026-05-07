from abc import ABC, abstractmethod
from .models import Transaction


class BaseTransactionStrategy(ABC):
    @abstractmethod
    def execute(self, request, product, form):
        pass


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction = Transaction()
        transaction.buyer = request.user.profile
        transaction.product = product
        transaction.amount = form.cleaned_data.get('amount')
        transaction.status = form.cleaned_data.get('status')
        if transaction.amount > transaction.product.stock:
            transaction.amount = transaction.product.stock
        transaction.product.stock = (transaction.product.stock
                                     - transaction.amount)
        transaction.product.save()
        transaction.save()
        return 'merchstore:cart-view'


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction_amount = form.cleaned_data.get('amount')
        if transaction_amount > product.stock:
            transaction_amount = product.stock
        request.session['pending'] = {
            'product_id': product.id,
            'amount': transaction_amount,
            'status': form.cleaned_data.get('status')
        }
        return 'login'
