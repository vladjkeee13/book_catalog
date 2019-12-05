from django.db.models import Count
from .models import Category


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def menu(request):
    cats = Category.objects.annotate(
        books_count=Count('book')).order_by('-books_count')[:20]
    return {'categories': list(chunks(cats, 5)), 'range': range(5)}
