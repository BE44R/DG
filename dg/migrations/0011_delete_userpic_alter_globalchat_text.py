# Generated by Django 4.0.2 on 2022-05-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dg', '0010_userpic'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPic',
        ),
        migrations.AlterField(
            model_name='globalchat',
            name='text',
            field=models.CharField(max_length=2500),
        ),
    ]
