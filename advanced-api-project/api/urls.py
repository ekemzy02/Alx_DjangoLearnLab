from django.urls import path
from .views import BookListView, BookCreateView, BookDeleteView, BookDetailView, BookUpdateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]