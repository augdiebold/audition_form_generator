# Generated by Django 3.2.9 on 2021-11-25 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_fieldsauditionbase_field_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditionbase',
            name='slug',
        ),
    ]