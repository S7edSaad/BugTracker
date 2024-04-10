# Generated by Django 5.0.3 on 2024-03-21 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0009_bug_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bug",
            name="date",
        ),
        migrations.AddField(
            model_name="bug",
            name="created",
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bug",
            name="ended",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bug",
            name="timetaken",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]