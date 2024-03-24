# Generated by Django 5.0 on 2024-03-24 22:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0029_alter_committee_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="committee",
            name="id",
        ),
        migrations.AlterField(
            model_name="committee",
            name="code",
            field=models.CharField(
                max_length=10, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]
