# Generated by Django 4.2 on 2024-05-09 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_following_user_follow_followed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='created_at',
            new_name='followed_at',
        ),
    ]
