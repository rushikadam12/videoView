# Generated by Django 5.1.4 on 2024-12-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.CharField(max_length=255),
        ),
    ]
