# Generated by Django 5.0.3 on 2024-03-17 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0006_alter_bug_severity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bug",
            name="Assign",
            field=models.CharField(max_length=122, null=True),
        ),
        migrations.AlterField(
            model_name="bug",
            name="Priority",
            field=models.CharField(max_length=122, null=True),
        ),
    ]
