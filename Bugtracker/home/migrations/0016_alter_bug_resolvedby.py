# Generated by Django 5.0.3 on 2024-03-21 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0015_alter_bug_resolvedby"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bug",
            name="resolvedby",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
