# Generated by Django 2.2.11 on 2021-03-18 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0040_auto_20190813_1556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rodent',
            options={'permissions': [('can_import', 'Can import from XLSX')]},
        ),
    ]