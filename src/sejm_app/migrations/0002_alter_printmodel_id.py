# Generated by Django 5.0 on 2023-12-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="printmodel",
            name="id",
            field=models.CharField(
                editable=False, max_length=13, primary_key=True, serialize=False
            ),
        ),
    ]