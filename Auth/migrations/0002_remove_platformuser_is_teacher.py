# Generated by Django 2.2.1 on 2019-05-15 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platformuser',
            name='is_teacher',
        ),
    ]
