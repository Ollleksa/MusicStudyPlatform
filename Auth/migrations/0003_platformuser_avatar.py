# Generated by Django 2.2.1 on 2019-05-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_remove_platformuser_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformuser',
            name='avatar',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]