# Generated by Django 2.1.8 on 2019-06-21 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0030_auto_20190621_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodent',
            name='zygosity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rodents', to='rodentdb.Zygosity'),
        ),
    ]