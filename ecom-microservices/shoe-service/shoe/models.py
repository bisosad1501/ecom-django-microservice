# book/models.py
from djongo import models
from django.core.validators import MinValueValidator

class BookFormat(models.TextChoices):
    PAPERBACK = 'PAPERBACK', 'Paperback'
    HARDCOVER = 'HARDCOVER', 'Hardcover'
    EBOOK = 'EBOOK', 'Ebook'
    AUDIOBOOK = 'AUDIOBOOK', 'Audiobook'

class Book(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.JSONField(default=list)
    translator = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    edition = models.CharField(max_length=100, null=True, blank=True)
    series = models.CharField(max_length=255, null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=50)
    book_format = models.CharField(max_length=20, choices=BookFormat.choices)
    isbn_13 = models.CharField(max_length=13, unique=True)
    reading_age = models.CharField(max_length=50, null=True, blank=True)
    page_count = models.IntegerField(validators=[MinValueValidator(1)])
    summary = models.TextField()
    table_of_contents = models.JSONField(default=list)
    sample_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'