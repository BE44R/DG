# Generated by Django 4.0.2 on 2022-03-26 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dg', '0006_shopkeys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
