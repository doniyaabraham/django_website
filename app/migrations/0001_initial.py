# Generated by Django 4.2.7 on 2023-12-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('phno', models.IntegerField()),
                ('username', models.CharField(max_length=18)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
    ]
