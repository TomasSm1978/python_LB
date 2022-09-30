from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import date, timedelta


def home(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_visits': num_visits,
    }
    return render(request, 'home.html', context=context)


def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})


class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query) | Q(publisher__name__icontains=query) | Q(publishing_date__icontains=query) | Q(genre__name__icontains=query) | Q(isbn_code__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    context_object_name = 'books'
    template_name = 'user_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).order_by('due_back')
        # return BookInstance.objects.filter(reader=self.request.user).filter(status__exact='p').order_by('due_back')


class BookByUserDetailView(LoginRequiredMixin, DetailView):
    model = BookInstance
    template_name = 'user_book.html'


class BookByUserCreateView(LoginRequiredMixin, CreateView):
    model = BookInstance
    fields = ['book', 'reader', 'status', 'due_back']
    success_url = "/books"
    template_name = 'user_book_form.html'

    def form_valid(self, form):
        # form.instance.reader = self.request.user
        return super().form_valid(form)


class BookByUserUpdateView(LoginRequiredMixin, UpdateView):
    model = BookInstance
    fields = ['book', 'reader', 'status', 'due_back']
    success_url = "/books/"
    template_name = 'user_book_form.html'

    # def form_valid(self, form):
    #     form.instance.reader = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader


class BookByUserUpdateView_2(LoginRequiredMixin, UpdateView):
    model = BookInstance
    fields = ['book']
    success_url = "/books/"
    template_name = 'user_book_form_2.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 'r'
        form.instance.due_back = date.today() + timedelta(days=10)
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader


class BookByUserUpdateView_3(LoginRequiredMixin, UpdateView):
    model = BookInstance
    fields = ['book']
    success_url = "/books/"
    template_name = 'user_book_form_3.html'

    def form_valid(self, form):
        form.instance.reader = None
        form.instance.status = 'a'
        form.instance.due_back = date.today() + timedelta(days=10)
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader


class BookByUserDeleteView(LoginRequiredMixin, DeleteView):
    model = BookInstance
    success_url = "/books/"
    template_name = 'user_book_delete.html'

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader