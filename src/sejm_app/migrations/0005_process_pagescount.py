# Generated by Django 5.0 on 2024-03-26 18:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0004_remove_printmodel_mps_remove_printmodel_club_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="process",
            name="pagesCount",
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
