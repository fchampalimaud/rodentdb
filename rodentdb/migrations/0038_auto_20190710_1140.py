# Generated by Django 2.1.8 on 2019-07-10 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0037_auto_20190621_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodent',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Public through Congento'),
        ),
    ]