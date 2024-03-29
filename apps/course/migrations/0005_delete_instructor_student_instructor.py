# Generated by Django 5.0.1 on 2024-01-31 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_textlesson_view_time_and_more'),
        ('users', '0006_remove_temporaryuser_users_tempo_email_9e1cd9_idx_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Instructor',
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.profile',),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
            ],
            options={
                'verbose_name': 'Course Instructor',
                'verbose_name_plural': 'Course Instructors',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.profile',),
        ),
    ]
