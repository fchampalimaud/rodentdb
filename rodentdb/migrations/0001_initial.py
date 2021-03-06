# Generated by Django 2.2 on 2019-04-26 14:44

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rodent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('species', models.CharField(choices=[('rat', 'Rat'), ('mouse', 'Mouse')], max_length=5)),
                ('strain_name', models.CharField(max_length=20)),
                ('common_name', models.CharField(max_length=20)),
                ('background', models.CharField(choices=[('c57bl', 'C57BL/6'), ('balb', 'Balb/c'), ('sv', '129sv'), ('fvb', 'FVB'), ('mixed', 'Mixed'), ('other', 'Other')], max_length=5)),
                ('background_other', models.CharField(blank=True, max_length=20, verbose_name='')),
                ('genotype', models.CharField(choices=[('wt', 'WT'), ('homo', 'Homo'), ('het', 'Het'), ('hemi', 'Hemi'), ('both', 'Homo/Het'), ('other', 'Other')], max_length=5)),
                ('genotype_other', models.CharField(blank=True, max_length=20, verbose_name='')),
                ('model_type', models.CharField(choices=[('wt', 'WT'), ('tg', 'Transgenic'), ('ko', 'KO'), ('cre', 'Cre/flox'), ('other', 'Other')], max_length=5)),
                ('model_type_other', models.CharField(blank=True, max_length=20, verbose_name='')),
                ('origin', models.CharField(max_length=20)),
                ('availability', models.CharField(choices=[('live', 'Live'), ('cryo', 'Cryopreserved'), ('both', 'Live & Cryopreserved'), ('none', 'Unavailable')], max_length=4)),
                ('comments', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('mta', models.BooleanField(default=False, verbose_name='MTA')),
            ],
            options={
                'verbose_name_plural': 'rodent',
            },
        ),
    ]
