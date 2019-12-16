from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from cart.models import Cart, CartItem
from catalog.models import Book


class CartView(DetailView):

    template_name = 'cart.html'

    def get_object(self, queryset=None):

        try:
            cart_id = self.request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
            self.request.session['total'] = cart.items.count()
        except:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
            cart = Cart.objects.get(id=cart_id)

        return cart


class AddToCartView(View):

    def get(self, request):

        try:
            cart_id = self.request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
            self.request.session['total'] = cart.items.count()
        except:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
            cart = Cart.objects.get(id=cart_id)

        book = Book.objects.get(id=request.GET['book_id'])
        cart.add_to_cart(book)

        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)

        cart.cart_total = new_cart_total
        cart.save()

        # return redirect(reverse('book', kwargs={'slug': book.slug}))
        return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


class RemoveItemFromCartView(View):

    def get(self, request):

        try:
            cart_id = self.request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
            self.request.session['total'] = cart.items.count()
        except:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
            cart = Cart.objects.get(id=cart_id)

        item = CartItem.objects.get(id=request.GET['item_id'])
        cart.remove_from_cart(item)

        # new_cart_total = 0.00
        # for item in cart.items.all():
        #     new_cart_total += float(item.item_total)
        #
        # cart.cart_total = new_cart_total
        # cart.save()

        return redirect('cart:cart')


class ChangeItemQuantity(View):

    def get(self, request):

        try:
            cart_id = self.request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
            self.request.session['total'] = cart.items.count()
        except:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
            cart = Cart.objects.get(id=cart_id)

        qty = request.GET['qty']
        item_id = request.GET['item_id']

        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.quantity = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.book.price)
        cart_item.save()

        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)

        cart.cart_total = new_cart_total
        cart.save()

        return JsonResponse({
            'cart_total': cart.items.count(),
            'item_total': cart_item.item_total,
            'cart_total_price': cart.cart_total
        })
