# Generated by Django 4.2.7 on 2023-12-27 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_userdetails_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='address',
            field=models.CharField(default='ersttavammkkk', max_length=10),
            preserve_default=False,
        ),
    ]
