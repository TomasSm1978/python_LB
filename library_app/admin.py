from django.contrib import admin
from .models import Genre, Author, Publisher, Book, BookInstance
import uuid

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    readonly_fields = ('id',)
    can_delete = False
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'reader', 'due_back', 'id')
    search_fields = ('id', 'book__title')
    list_editable = ('due_back', 'status')
    fieldsets = (
        ('General', {'fields': ('id', 'book')}),
        ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    )


admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

