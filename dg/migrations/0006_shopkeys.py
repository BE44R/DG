# Generated by Django 4.0.2 on 2022-03-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dg', '0005_userbalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('money', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
        ),
    ]
