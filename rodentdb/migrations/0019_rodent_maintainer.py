# Generated by Django 2.1.8 on 2019-06-11 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rodentdb', '0018_rodent_line_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='rodent',
            name='maintainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
