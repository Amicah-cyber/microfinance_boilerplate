# Generated by Django 4.0.5 on 2022-09-09 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
    ]
