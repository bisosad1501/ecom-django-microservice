# Generated by Django 4.2.20 on 2025-04-02 19:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_id', models.CharField(db_index=True, max_length=24)),
                ('user_id', models.UUIDField(db_index=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(blank=True, max_length=200)),
                ('comment', models.TextField(blank=True)),
                ('media_urls', models.JSONField(blank=True, default=list)),
                ('helpful_votes', models.IntegerField(default=0)),
                ('not_helpful_votes', models.IntegerField(default=0)),
                ('report_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_edited', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VerifiedReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_id', models.CharField(db_index=True, max_length=24)),
                ('user_id', models.UUIDField(db_index=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(blank=True, max_length=200)),
                ('comment', models.TextField(blank=True)),
                ('media_urls', models.JSONField(blank=True, default=list)),
                ('helpful_votes', models.IntegerField(default=0)),
                ('not_helpful_votes', models.IntegerField(default=0)),
                ('report_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_edited', models.BooleanField(default=False)),
                ('order_id', models.CharField(max_length=100)),
                ('purchase_date', models.DateTimeField()),
                ('quality_rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('value_rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('shipping_rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('seller_response', models.TextField(blank=True, null=True)),
                ('seller_response_date', models.DateTimeField(null=True)),
            ],
            options={
                'unique_together': {('product_id', 'user_id', 'order_id')},
            },
        ),
        migrations.CreateModel(
            name='ReviewComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(db_index=True)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('general_review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.generalreview')),
                ('verified_review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.verifiedreview')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='generalreview',
            index=models.Index(fields=['product_id'], name='reviews_gen_product_fd8f73_idx'),
        ),
        migrations.AddIndex(
            model_name='generalreview',
            index=models.Index(fields=['user_id'], name='reviews_gen_user_id_e743d5_idx'),
        ),
        migrations.AddIndex(
            model_name='generalreview',
            index=models.Index(fields=['rating'], name='reviews_gen_rating_4b6a66_idx'),
        ),
        migrations.AddIndex(
            model_name='generalreview',
            index=models.Index(fields=['created_at'], name='reviews_gen_created_bcc6f2_idx'),
        ),
    ]
