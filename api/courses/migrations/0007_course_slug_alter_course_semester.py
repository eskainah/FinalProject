# Generated by Django 5.0.8 on 2024-12-04 09:44

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_semester'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')], max_length=50),
        ),
    ]
