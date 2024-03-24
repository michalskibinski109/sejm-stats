# Generated by Django 5.0 on 2024-03-24 21:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0026_alter_committee_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="committee",
            name="type",
            field=models.CharField(
                choices=[
                    ("Nadzwyczajna", "Nadzwyczajna"),
                    ("ŚledczaŚledcza", "Investigative"),
                    ("StałaStała", "Standing"),
                ],
                default="StałaStała",
                max_length=50,
            ),
        ),
    ]
