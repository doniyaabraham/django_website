# Generated by Django 5.0.1 on 2024-01-31 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='status',
            field=models.CharField(default='Shipped', max_length=20),
        ),
    ]