# Generated by Django 5.1.2 on 2024-10-12 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_genre_play_play_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='play',
            old_name='genre',
            new_name='genres',
        ),
    ]
