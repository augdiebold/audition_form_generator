# Generated by Django 3.2.9 on 2021-11-08 18:24

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20211102_2059'),
    ]

    operations = [
        HStoreExtension(),
        migrations.RenameField(
            model_name='audition',
            old_name='date',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='audition',
            name='data',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={'a': 'b'}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fieldsauditionbase',
            name='field_type',
            field=models.CharField(choices=[('CharField', 'CharField'), ('EmailField', 'EmailField'), ('ChoiceField', 'ChoiceField')], max_length=100),
        ),
    ]
