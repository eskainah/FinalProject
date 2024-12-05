# Generated by Django 5.0.8 on 2024-12-03 19:50

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_course_instructor_id_input_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall <function current_year at 0x7481129aac20>', 'Fall <function current_year at 0x7481129aac20>'), ('Spring <function current_year at 0x7481129aac20>', 'Spring <function current_year at 0x7481129aac20>'), ('Summer <function current_year at 0x7481129aac20>', 'Summer <function current_year at 0x7481129aac20>')], max_length=50, validators=[courses.models.validate_semester]),
        ),
    ]