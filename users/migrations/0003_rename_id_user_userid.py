# Generated by Django 5.0.6 on 2024-07-07 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_userid_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='userId',
        ),
    ]
