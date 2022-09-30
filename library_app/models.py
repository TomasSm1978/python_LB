from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField('Genre name', max_length=200, help_text='Enter genre')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField('Name', max_length=100)
    last_name = models.CharField('Surname', max_length=100)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def display_books(self):
        return ', '.join(book.title for book in self.books.all()[:3])

    display_books.short_description = 'Books'


class Publisher(models.Model):
    name = models.CharField('Publisher name', max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField('Title', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    publishing_date = models.DateField('Book publishing date', null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Choose genre')
    isbn_code = models.CharField('ISBN', max_length=13, help_text='13 symbols <a href="https://www.isbn-international.org/content/what-isbn">What is ISBN code?</a>')
    cover = models.ImageField('Cover', upload_to='covers', null=True, blank=True)

    def get_absolute_url(self):
       return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for book copy')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    due_back = models.DateField('Due back', null=True, blank=True)

    LOAN_STATUS = (

        ('a', 'Available'),
        ('r', 'Reserved'),
        ('b', 'Borrowed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Status')
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
       return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def form_valid(self, form):
        form.instance.reader = User.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)