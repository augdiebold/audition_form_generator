# Generated by Django 3.2.9 on 2021-11-25 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_audition_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldsauditionbase',
            name='field_type',
            field=models.CharField(choices=[('CharField', 'CharField'), ('EmailField', 'EmailField'), ('ChoiceField', 'ChoiceField'), ('BooleanField', 'BooleanField'), ('URLField', 'URLField'), ('EmailField', 'EmailField')], max_length=100),
        ),
    ]