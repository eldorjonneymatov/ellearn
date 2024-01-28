# Generated by Django 5.0.1 on 2024-01-28 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_textlesson_options_alter_videolesson_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textlesson',
            name='description',
        ),
        migrations.RemoveField(
            model_name='videolesson',
            name='description',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug'),
        ),
    ]
