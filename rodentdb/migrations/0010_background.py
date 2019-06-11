# Generated by Django 2.1.8 on 2019-06-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0009_auto_20190611_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'background',
                'verbose_name_plural': 'backgrounds',
                'ordering': ['name'],
            },
        ),
    ]