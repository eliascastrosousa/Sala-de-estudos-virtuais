# Generated by Django 4.1.7 on 2023-06-18 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_announcement_updated_room_updated_roadmap_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadmap',
            name='content',
            field=models.TextField(),
        ),
    ]
