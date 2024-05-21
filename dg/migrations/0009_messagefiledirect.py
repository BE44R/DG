# Generated by Django 4.0.2 on 2022-05-14 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dg', '0008_messagefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageFileDirect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, default=None, null=True, upload_to='direct_chat')),
                ('name', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('size', models.IntegerField(blank=True, default=None, null=True)),
                ('message', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='dg.message')),
            ],
        ),
    ]