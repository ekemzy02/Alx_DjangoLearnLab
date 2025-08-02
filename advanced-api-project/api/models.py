from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
       
    def __str__(self):
        return self.name
# The Author model stores the name of the author. 
  
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
# The Book model stores the name and publication year of the book.
    def __str__(self):
        return self.title
# Create your models here.
