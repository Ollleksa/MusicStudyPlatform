# Generated by Django 2.2.1 on 2019-05-16 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lesson', '0002_auto_20190515_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
