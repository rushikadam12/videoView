# Generated by Django 5.1.4 on 2024-12-29 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_users_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.URLField(max_length=255),
        ),
    ]