# Generated by Django 5.2.1 on 2025-05-21 21:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_post_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
