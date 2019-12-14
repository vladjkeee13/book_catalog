from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.contrib import messages

from .models import Book, Category, Reviews
from .forms import ReviewForm, RegistrationForm, LoginForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all().order_by('-id')[:5]
        art_books = Book.objects.filter(cat__name='Art').order_by('id')[:5]
        children_books = Book.objects.filter(cat__name='Childrens').order_by('id')[:8]
        context.update({
            'books': books,
            'art_books': art_books,
            'children_books': children_books
        })
        return context


class CatalogView(ListView, SingleObjectMixin):
    template_name = 'catalog.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        author = self.request.GET.get('author')
        if author:
            return Book.objects.filter(
                cat=self.object, author=author)
        return Book.objects.filter(cat=self.object).prefetch_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = set([b.author for b in Book.objects.filter(cat=self.object.id)])
        authors = list(authors)
        authors.sort()
        context['authors'] = authors[:20]
        return context


@method_decorator(csrf_protect, name='dispatch')
class BookView(DetailView):
    template_name = 'book.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['art_books'] = Book.objects.all()[10:20]
        context['reviews'] = Reviews.objects.filter(
            book=self.object).order_by('-published')[:10]
        return context

    # def post(self, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.form = ReviewForm(self.request.POST)
    #
    #     context = self.get_context_data(**kwargs)
    #
    #     if self.form.is_valid():
    #         self.form.cleaned_data['book'] = self.object
    #         Reviews.objects.create(**self.form.cleaned_data)
    #         messages.add_message(
    #             self.request, messages.INFO,
    #             'Thanks! Your review is on moderation.'
    #         )
    #     else:
    #         context['form'] = self.form
    #         messages.add_message(
    #             self.request, messages.INFO,
    #             'Incorrect data'
    #         )
    #     return self.render_to_response(context)


class SearchView(ListView):
    template_name = 'catalog.html'
    paginate_by = 30

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(name__contains=query)
        else:
            return Http404()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        authors = set([b.author for b in self.get_queryset()])
        authors = list(authors)
        authors.sort()
        context['authors'] = authors[:20]

        return context


def robots_view(request):
    return render(request, 'robots.txt', {}, content_type="text/plain")


# @method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class AddCommentView(CreateView):

    form_class = ReviewForm

    def form_valid(self, form):

        response = super().form_valid(form)
        book = Book.objects.get(slug=self.kwargs['slug'])
        self.object = form.save(user=self.request.user, book=book)

        return response

    def get_success_url(self):
        return reverse('book', kwargs={'slug': self.kwargs.get('slug')})


class RegistrationView(FormView):

    template_name = 'registration.html'
    form_class = RegistrationForm

    def form_valid(self, form, backend='django.contrib.auth.backends.ModelBackend'):

        form.save()

        user = User.objects.get(username=form.cleaned_data['username'])

        if user:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('/')


class LoginView(FormView):

    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        login_user = authenticate(username=username, password=password)

        if login_user:
            login(self.request, login_user)

        return redirect('/')
