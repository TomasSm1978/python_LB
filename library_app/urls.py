from django.urls import path
from . import views


urlpatterns = [
   path('', views.home, name="home"),
   path('authors/', views.authors, name="authors"),
   path('authors/<int:author_id>', views.author, name='author'),
   path('books/', views.BookListView.as_view(), name="books"),
   path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
   path('search/', views.search, name='search'),
   path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
   path('mybooks/new/', views.BookByUserCreateView.as_view(), name='my-borrowed-new'),
   path('mybooks/<str:pk>/update', views.BookByUserUpdateView.as_view(), name='my-book-update'),
   path('mybooks_2/<str:pk>/update', views.BookByUserUpdateView_2.as_view(), name='my-book-update-2'),
   path('mybooks_3/<str:pk>/update', views.BookByUserUpdateView_3.as_view(), name='my-book-update-3'),
   path('mybooks/<str:pk>/delete', views.BookByUserDeleteView.as_view(), name='my-book-delete'),
]