# Generated by Django 5.0 on 2023-12-22 18:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0006_alter_process_ue"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="process",
            name="term",
        ),
    ]