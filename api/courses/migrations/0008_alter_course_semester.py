# Generated by Django 5.0.8 on 2024-12-04 10:31

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_slug_alter_course_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall <function current_year at 0x7602d2882c20>', 'Fall <function current_year at 0x7602d2882c20>'), ('Spring <function current_year at 0x7602d2882c20>', 'Spring <function current_year at 0x7602d2882c20>'), ('Summer <function current_year at 0x7602d2882c20>', 'Summer <function current_year at 0x7602d2882c20>')], max_length=50, validators=[courses.models.validate_semester]),
        ),
    ]