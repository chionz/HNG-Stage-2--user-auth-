# Generated by Django 5.0.6 on 2024-07-07 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
    ]
