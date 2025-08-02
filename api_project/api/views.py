from .serializers import BookSerializer
from rest_framework import generics, viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all()
    
class BookViewSet(viewsets.ModelViewSet): 
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Book.objects.all()
    

# Create your views here.
