# Generated by Django 5.2.1 on 2025-07-07 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_post_rating_post_ratings_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
