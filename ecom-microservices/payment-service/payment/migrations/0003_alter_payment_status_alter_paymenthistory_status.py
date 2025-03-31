# Generated by Django 4.2.7 on 2025-03-30 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_status_alter_paymenthistory_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Chờ thanh toán'), ('completed', 'Đã thanh toán'), ('failed', 'Thanh toán thất bại'), ('refunded', 'Đã hoàn tiền')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='status',
            field=models.CharField(choices=[('pending', 'Chờ thanh toán'), ('completed', 'Đã thanh toán'), ('failed', 'Thanh toán thất bại'), ('refunded', 'Đã hoàn tiền')], max_length=20),
        ),
    ]
