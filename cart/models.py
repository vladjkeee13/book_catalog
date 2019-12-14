from django.contrib.auth.models import User
from django.db import models


class CartItem(models.Model):

    book = models.ForeignKey('catalog.Book', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return "Cart item for book {0}".format(self.book.name)


class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, book):

        cart = self
        new_item, _ = CartItem.objects.get_or_create(book=book)
        new_item.item_total = book.price
        new_item.save()

        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, item):

        cart = self

        if item in cart.items.all():
            cart.items.remove(item)
            cart.save()

#
# class Wishlist(models.Model):
#
#     product = models.ManyToManyField('product.Product')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
