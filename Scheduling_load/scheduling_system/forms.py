from django import forms
from .models import ProgramSchedule

class ProgramScheduleForm(forms.ModelForm):
    class Meta:
        model = ProgramSchedule
        fields = ['instructor_name', 'course_code', 'course_name', 'credit_hours', 
                  'semester', 'program_name', 'program_code', 'room_number', 
                  'room_type', 'building_name', 'campus_name', 'day', 
                  'start_time', 'end_time', 'year_level', 'section', 'shift']