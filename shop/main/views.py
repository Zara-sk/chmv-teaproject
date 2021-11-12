import operator

from functools import reduce
from itertools import chain

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.db.models import Q


from .models import *
from .mixins import CartMixin
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart

from specs.models import ProductFeatures


import json



class HomepageView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        new_products = Product.objects.all().order_by('-id')[:10]
        stea = Product.objects.filter(category=1).order_by('?')[:6]
        sdrink = Product.objects.filter(category=2).order_by('?')[:6]

        context = {
            'categories': categories,
            'new_products': new_products,
            'stea': stea,
            'sdrink': sdrink,
            'cart': self.cart,
        }

        return render(request, 'homepage.html', context)


class ProductDetailView(CartMixin, DetailView):

    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['categories'] = Category.objects.all()
        return context

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CartMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('search')
        category = self.get_object()

        context['cart'] = self.cart
        context['categories'] = self.model.objects.all()

        if not query and not self.request.GET:

            context['category_products'] = category.product_set.all()
            return context

        if query:
            
            q_list = Q()
            q_list |= Q(title__icontains=query)
            q_list |= Q(title__icontains=query.title())
            products = category.product_set.filter(q_list)

            context['category_products'] = products

            return context

        url_kwargs = {}

        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)

            else:
                url_kwargs[item] = self.request.GET.get(item)

        q_list = []

        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_list.append(Q(**{'value__in': value}))

            else:
                q_list.append(Q(**{'value': value}))

        pf_list = []
        for q_cond in q_list:
            pf_list.append(ProductFeatures.objects.filter(q_cond).prefetch_related('product', 'feature').values('product_id'))

        products = Product.objects.all()
        for pf in pf_list:
            products= products.filter(id__in=[pf_['product_id'] for pf_ in pf], category=category)

        context['category_products'] = products

        return context



class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        product_slug = kwargs.get('slug')

        product = Product.objects.get(slug=product_slug)

        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner,
            cart=self.cart,
            product=product
        )

        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)

        messages.add_message(request, messages.INFO, "Товар добавлен в корзину!")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')

        product = Product.objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner,
            cart=self.cart,
            product=product
        )

        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)

        return HttpResponse(
            json.dumps('successful!'),
            content_type="application/json"
        )


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):

        product_slug = kwargs.get('slug')

        product = Product.objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner,
            cart=self.cart,
            product=product
        )

        qty = int(request.POST.get('qty'))

        if 1 <= cart_product.quantity + qty <= 50:
            cart_product.quantity += qty
            cart_product.save()
        recalc_cart(self.cart)

        return HttpResponse(
            json.dumps('successful!'),
            content_type="application/json"
        )


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
        }

        return render(request, 'cart.html', context)

class CheckOutView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()

        form = OrderForm(request.POST or None)

        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
        }

        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'form': form,
            'categories': Category.objects.all(),
            'cart': self.cart,
        }
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']

            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, "Заказ оформлен!")
            return HttpResponseRedirect('/')
        return render(request, 'checkout.html', context)


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'categories': Category.objects.all(),
            'cart': self.cart,
        }

        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'categories': Category.objects.all(),
            'cart': self.cart,
        }
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(email=email, password=password)
            if user:
                login(request, user=user)
                return HttpResponseRedirect('/')

        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'categories': Category.objects.all(),
            'cart': self.cart,
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'categories': Category.objects.all(),
            'cart': self.cart,
        }

        if form.is_valid():
            new_user = form.save(commit=False)
            cl_data = form.cleaned_data

            new_user.email = cl_data['email']
            # new_user.first_name = cl_data['first_name']
            # new_user.last_name = cl_data['last_name']
            # new_user.phone = cl_data['phone']
            # new_user.address = cl_data['address']

            new_user.save()
            new_user.set_password(cl_data['password'])
            new_user.save()

            Customer.objects.create(
                user=new_user
            )

            user = authenticate(email=cl_data['email'], password=cl_data['password'])
            login(request, user=user)
            return HttpResponseRedirect('/')

        return render(request, 'registration.html', context)


class OrdersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        context = {
            'categories': Category.objects.all(),
            'orders': orders,
            'cart': self.cart
        }

        return render(request, 'orders.html', context)