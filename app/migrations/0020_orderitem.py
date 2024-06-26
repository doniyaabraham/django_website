# Generated by Django 5.0.1 on 2024-02-07 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('orderdet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.products')),
            ],
        ),
    ]
