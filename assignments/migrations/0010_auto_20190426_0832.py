# Generated by Django 2.2 on 2019-04-26 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190425_0556'),
        ('assignments', '0009_auto_20190425_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='VM',
            fields=[
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Teacher')),
                ('port_used', models.IntegerField(verbose_name='Port Used')),
            ],
        ),
        migrations.AlterField(
            model_name='environment',
            name='bash_file_url',
            field=models.FilePathField(path='/home/abhey/ASP/assignments/env'),
        ),
    ]
