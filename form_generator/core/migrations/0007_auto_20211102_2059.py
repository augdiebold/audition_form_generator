# Generated by Django 3.2.9 on 2021-11-02 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_fieldsauditionbase_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditionbase',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='fieldsauditionbase',
            name='choices',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
