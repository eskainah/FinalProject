# Generated by Django 5.0.8 on 2024-10-22 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_records', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='teacher_id',
            new_name='instructor_id',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='teacher_name',
            new_name='instructor_name',
        ),
    ]
