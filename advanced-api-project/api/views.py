from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, filters
from .serializers import BookSerializer
from .models import Book, Author
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
import django_filters

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.NumberFilter(field_name='publication_year')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def create(self, serializer):
        author_name =self.request.data.get('Dan Brown')
        author = Author.objects.get_or_create(name=author_name)[0]
        serializer.save(author=author)

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = BookFilter
    ordering_fields = ['title', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# only authenticated users can update, delete and add books in this application.
# Create your views here.
