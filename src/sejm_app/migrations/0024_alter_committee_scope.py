# Generated by Django 5.0 on 2024-03-24 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0023_committee_committeemember"),
    ]

    operations = [
        migrations.AlterField(
            model_name="committee",
            name="scope",
            field=models.TextField(null=True),
        ),
    ]
