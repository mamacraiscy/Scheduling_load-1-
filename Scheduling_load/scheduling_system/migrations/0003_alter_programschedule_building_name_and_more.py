# Generated by Django 5.1.1 on 2024-11-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduling_system", "0002_programschedule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programschedule",
            name="building_name",
            field=models.CharField(default="Default Building", max_length=100),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="campus_name",
            field=models.CharField(default="Default Campus", max_length=100),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="course_code",
            field=models.CharField(default="N/A", max_length=50),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="course_name",
            field=models.CharField(default="Untitled Course", max_length=200),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="credit_hours",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="day",
            field=models.CharField(default="Monday", max_length=20),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="end_time",
            field=models.TimeField(default="00:00:00"),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="instructor_name",
            field=models.CharField(default="Unknown Instructor", max_length=200),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="program_code",
            field=models.CharField(default="N/A", max_length=50),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="program_name",
            field=models.CharField(default="General Program", max_length=100),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="room_number",
            field=models.CharField(default="000", max_length=100),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="room_type",
            field=models.CharField(default="N/A", max_length=50),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="section",
            field=models.CharField(default="Default Section", max_length=100),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="semester",
            field=models.CharField(default="N/A", max_length=50),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="shift",
            field=models.CharField(default="Day", max_length=20),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="start_time",
            field=models.TimeField(default="00:00:00"),
        ),
        migrations.AlterField(
            model_name="programschedule",
            name="year_level",
            field=models.CharField(default="1st Year", max_length=50),
        ),
    ]
