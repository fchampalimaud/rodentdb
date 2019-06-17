# Generated by Django 2.1.8 on 2019-06-17 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodentdb', '0022_auto_20190611_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoatColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'coat color',
                'verbose_name_plural': 'coat colors',
                'ordering': ['name'],
            },
        ),
    ]
