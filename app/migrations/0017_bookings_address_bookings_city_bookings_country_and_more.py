# Generated by Django 5.0.1 on 2024-02-04 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_passwordreset'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='address',
            field=models.CharField(max_length=150, null='amayoor'),
            preserve_default='amayoor',
        ),
        migrations.AddField(
            model_name='bookings',
            name='city',
            field=models.CharField(max_length=150, null='kochi'),
            preserve_default='kochi',
        ),
        migrations.AddField(
            model_name='bookings',
            name='country',
            field=models.CharField(max_length=150, null='india'),
            preserve_default='india',
        ),
        migrations.AddField(
            model_name='bookings',
            name='pincode',
            field=models.IntegerField(default='686010', max_length=6),
        ),
        migrations.AddField(
            model_name='bookings',
            name='state',
            field=models.CharField(max_length=150, null='kerala'),
            preserve_default='kerala',
        ),
    ]
