# Generated by Django 5.0.1 on 2024-01-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_cart_quantity_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='track',
            field=models.CharField(default='Not Paid', max_length=20),
        ),
    ]