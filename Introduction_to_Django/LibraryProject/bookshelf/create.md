# Create Operation

Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
#Expected Output:
#<Book: 1949 by George Orwell (1949)>
