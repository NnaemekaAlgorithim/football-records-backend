# Generated by Django 5.1.1 on 2024-09-17 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football_app", "0010_remove_player_age_player_date_of_birth"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="user_age",
        ),
        migrations.AddField(
            model_name="customuser",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
