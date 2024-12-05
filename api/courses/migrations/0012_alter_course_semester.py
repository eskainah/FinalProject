# Generated by Django 5.0.8 on 2024-12-04 17:42

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_course_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall <function current_year at 0x77a9a4fcac20>', 'Fall <function current_year at 0x77a9a4fcac20>'), ('Spring <function current_year at 0x77a9a4fcac20>', 'Spring <function current_year at 0x77a9a4fcac20>'), ('Summer <function current_year at 0x77a9a4fcac20>', 'Summer <function current_year at 0x77a9a4fcac20>')], max_length=50, validators=[courses.models.validate_semester]),
        ),
    ]