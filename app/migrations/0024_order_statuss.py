# Generated by Django 5.0.1 on 2024-02-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_remove_bookings_pincode_products_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='statuss',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Dispatch'), (3, 'On the way'), (4, 'Delivered'), (5, 'Cancelled')], default=1),
        ),
    ]