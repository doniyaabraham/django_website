# Generated by Django 5.0.1 on 2024-02-20 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_order_statuss'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image1',
            field=models.FileField(default='image1', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='image2',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='image3',
            field=models.FileField(default='hi', upload_to=''),
            preserve_default=False,
        ),
    ]
