from django.db.models import Count

from cart.models import Cart
from .models import Category


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def menu(request):
    cats = Category.objects.annotate(
        books_count=Count('book')).order_by('-books_count')[:20]
    return {'categories': list(chunks(cats, 5)), 'range': range(5)}


def cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return {'cart': cart}
