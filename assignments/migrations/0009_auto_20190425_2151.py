# Generated by Django 2.2 on 2019-04-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0008_auto_20190425_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='bash_file_url',
            field=models.FilePathField(path='/home/abhey/ASP/assignments\\env'),
        ),
    ]
