# Generated by Django 2.2 on 2019-04-25 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='bash_file_url',
            field=models.FilePathField(path='E:\\Sem_8\\Major_Project\\ASP\\assignments\\env'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='env_id',
            field=models.CharField(choices=[('ap_sp', 'Apache Spark'), ('yn_mp', 'Yarn/Map Reduce'), ('hb', 'HBase')], default='ap-sp', max_length=10, primary_key=True, serialize=False, verbose_name='Environment'),
        ),
    ]
