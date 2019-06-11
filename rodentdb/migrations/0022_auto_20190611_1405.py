# Generated by Django 2.1.8 on 2019-06-11 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0021_rodent_ownership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodent',
            name='background',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rodents', to='rodentdb.Background'),
        ),
    ]
