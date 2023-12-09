# Generated by Django 4.2.5 on 2023-12-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="vote",
            field=models.CharField(
                blank=True,
                choices=[("YES", "Yes"), ("NO", "No"), ("ABSTAIN", "Abstain")],
                help_text="Vote option",
                max_length=255,
                null=True,
            ),
        ),
        migrations.DeleteModel(
            name="VotingOption",
        ),
    ]
