# Generated by Django 4.2.5 on 2023-10-10 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_profile_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
