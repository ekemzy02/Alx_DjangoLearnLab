import os
import django

#  Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')  
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# list books by author:
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.objects.filter(author=author)
        print(f'Books by {author_name}:')
        for book in books:
            print(f'- {book.title}')
    except Author.DoesNotExist:
        print(f'Author {author_name} does not exist.')

# List of all the books:
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f'Books in {library_name}:')
        for book in books:
            print(f'- {book.title}')
    except Library.DoesNotExist:
        print(f'Library {library_name} does not exist.')

# Retrieve operation:
def get_librarian_for_library(library_name):
    try:
        library = Librarian.objects.get(library=library_name)
        librarian = library.librarian
        print(f'Librarian for {library_name}: {librarian.name}')
    except Library.DoesNotExist:
        print(f'Library {library_name} does not exist.')
    except Librarian.DoesNotExist:
        print(f'No librarian assigned to {library_name}.')

# instances usage
if __name__ == '__main__':
    get_books_by_author('Charles Dickens')  
    get_books_in_library('Kwa-Thema Library') 
    get_librarian_for_library('Kwa-Thema Library')