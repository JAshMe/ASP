# Generated by Django 2.2 on 2019-04-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_auto_20190425_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assign_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Assignment ID'),
        ),
    ]
