# relationship_app/migrations/000X_add_permissions_to_book.py

from django.db import migrations

def create_permissions(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    book_content_type = ContentType.objects.get_for_model('Book')

    Permission.objects.create(
        codename='can_add_book',
        name='Can add book',
        content_type=book_content_type,
    )
    Permission.objects.create(
        codename='can_change_book',
        name='Can change book',
        content_type=book_content_type,
    )
    Permission.objects.create(
        codename='can_delete_book',
        name='Can delete book',
        content_type=book_content_type,
    )

class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0001_initial'),  # Adjust depending on the latest migration file
        ('auth', '0012_auto_20200422_1043'),  # This should be the latest migration for auth
    ]

    operations = [
        migrations.RunPython(create_permissions),
    ]
