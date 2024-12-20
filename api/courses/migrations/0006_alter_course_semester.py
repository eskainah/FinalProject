# Generated by Django 5.0.8 on 2024-12-04 07:44

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_course_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall <function current_year at 0x7a89e183ac20>', 'Fall <function current_year at 0x7a89e183ac20>'), ('Spring <function current_year at 0x7a89e183ac20>', 'Spring <function current_year at 0x7a89e183ac20>'), ('Summer <function current_year at 0x7a89e183ac20>', 'Summer <function current_year at 0x7a89e183ac20>')], max_length=50, validators=[courses.models.validate_semester]),
        ),
    ]
