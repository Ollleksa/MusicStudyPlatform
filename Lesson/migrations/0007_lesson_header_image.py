# Generated by Django 2.2.1 on 2019-05-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lesson', '0006_auto_20190520_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
