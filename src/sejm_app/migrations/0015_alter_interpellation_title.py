# Generated by Django 5.0 on 2024-03-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sejm_app", "0014_rename_body_link_reply_bodylink_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="interpellation",
            name="title",
            field=models.CharField(
                help_text="Title of the interpellation", max_length=512, null=True
            ),
        ),
    ]