# Generated by Django 3.2.20 on 2025-03-29 11:05

import django.core.validators
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('product_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('authors', djongo.models.fields.JSONField(default=list)),
                ('translator', models.CharField(blank=True, max_length=255, null=True)),
                ('publisher', models.CharField(max_length=255)),
                ('publication_date', models.DateField()),
                ('edition', models.CharField(blank=True, max_length=100, null=True)),
                ('series', models.CharField(blank=True, max_length=255, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('language', models.CharField(max_length=50)),
                ('book_format', models.CharField(choices=[('PAPERBACK', 'Paperback'), ('HARDCOVER', 'Hardcover'), ('EBOOK', 'Ebook'), ('AUDIOBOOK', 'Audiobook')], max_length=20)),
                ('isbn_13', models.CharField(max_length=13, unique=True)),
                ('reading_age', models.CharField(blank=True, max_length=50, null=True)),
                ('page_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('summary', models.TextField()),
                ('table_of_contents', djongo.models.fields.JSONField(default=list)),
                ('sample_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]
