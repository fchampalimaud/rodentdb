# Generated by Django 2.2.1 on 2019-05-06 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('rodentdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rodent',
            name='lab',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='Ownership'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RodentPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewonly', models.BooleanField(verbose_name='Read only access')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('rodent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rodentdb.Rodent')),
            ],
            options={
                'verbose_name': 'Rodent permission',
                'verbose_name_plural': 'Rodents permissions',
                'unique_together': {('rodent', 'group')},
            },
        ),
    ]
