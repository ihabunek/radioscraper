# Generated by Django 3.0.4 on 2020-04-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loaders', '0002_auto_20200311_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loaderfailure',
            name='type',
        ),
        migrations.AlterField(
            model_name='requestdata',
            name='method',
            field=models.CharField(max_length=10),
        ),
    ]
