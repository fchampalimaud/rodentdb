# Generated by Django 2.2.1 on 2019-05-08 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0003_auto_20190507_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='rodent',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Public'),
        ),
    ]