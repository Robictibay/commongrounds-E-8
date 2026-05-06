from abc import ABC, abstractmethod
from django.shortcuts import redirect
from .models import Transaction

class BaseTransactionStrategy(ABC):
    def execute(self, request, product, form):
        pass

class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction = Transaction()
        transaction.buyer = request.user.profile
        transaction.product = product
        transaction.amount = form.cleaned_data.get('amount')
        transaction.status = form.cleaned_data.get('status')  
        transaction.product.stock = transaction.product.stock - transaction.amount
        transaction.product.save()      
        transaction.save()
        return 'merchstore:cart-view'
        

class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session['pending_transaction'] = {
            'product_id': product.id,
            'amount': form.cleaned_data.get('amount'),
            'status': form.cleaned_data.get('status')
        }
        return 'login'