# Generated by Django 2.1.11 on 2019-08-13 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0038_auto_20190710_1140'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rodentpermission',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='rodentpermission',
            name='group',
        ),
        migrations.RemoveField(
            model_name='rodentpermission',
            name='rodent',
        ),
        migrations.DeleteModel(
            name='RodentPermission',
        ),
    ]