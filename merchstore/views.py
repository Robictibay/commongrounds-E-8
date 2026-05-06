from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from accounts.mixins import RoleRequiredMixin
from accounts.models import Profile
from .models import Product, Transaction
from .forms import ProductForm, TransactionForm


class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_authenticated:
            context['all_products'] = Product.objects.exclude(owner__user__exact=user)
            context['user_products'] = Product.objects.filter(owner__user__exact=user)
        else:
            context['all_products'] = Product.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            if self.request.user.is_authenticated:
                transaction = Transaction()
                transaction.buyer = self.request.user.profile
                transaction.product = super().get_object()
                transaction.amount = form.cleaned_data.get('amount')
                transaction.status = form.cleaned_data.get('status')  
                transaction.product.stock = transaction.product.stock - transaction.amount
                transaction.product.save()      
                transaction.save()
                return redirect('merchstore:item-list')
            else:
                return redirect('login')
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    template_name = 'merchstore/product_form.html'
    required_role = 'Market Seller'
    form_class = ProductForm

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.owner = self.request.user.profile
        self.object.save()
        return response


class ProductUpdateview(RoleRequiredMixin, UpdateView):
    model = Product
    template_name = 'merchstore/product_form.html'
    required_role = 'Market Seller'
    form_class = ProductForm


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart_view.html"
    redirect_field_name = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Transaction.objects.filter(buyer__user__exact=self.request.user)
        unique_owner_ids = Transaction.objects.filter(buyer__user__exact=self.request.user).order_by().values('product__owner').distinct()
        context['owners'] = Profile.objects.filter(id__in=unique_owner_ids)
        return context


class TransactionsList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/transaction_list.html"
    redirect_field_name = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Transaction.objects.filter(product__owner__user__exact=self.request.user)
        unique_buyer_ids = Transaction.objects.filter(product__owner__user__exact=self.request.user).order_by().values('buyer').distinct()
        context['buyers'] = Profile.objects.filter(id__in=unique_buyer_ids)
        return context