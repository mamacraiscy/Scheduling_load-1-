from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import InstructorData, InstructorCourse, Program, Room, Campus, Building, Room, ProgramSchedule
from .forms import ProgramScheduleForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def home(request):
    return render(request, 'instructors_frontend/index.html')  # Original home page

# Create teaching load page
def create_teaching_load(request):
    return render(request, 'instructors_frontend/create_load.html')  # New page for teaching load

def teaching_load(request):
    return render(request,'instructors_frontend/teaching_load.html')

def section(request):
    return render(request,'instructors_frontend/section.html')

def search_instructors(request):
    if request.method == "GET":
        query = request.GET.get('q', '').strip()  # Get the search query
        filter_type = request.GET.get('filter', 'ALL')  # Get the filter type (ALL, regular, cos)

        # Debugging: Print query and filter
        print(f"Search Query: {query}, Filter: {filter_type}")

        # Start with all instructors
        instructors = InstructorData.objects.all()

        # Apply filtering logic based on employment type
        if filter_type == 'REGULAR':
            instructors = instructors.filter(employment_type='REGULAR')
        elif filter_type == 'COS':
            instructors = instructors.filter(employment_type='COS')

        # Apply query if present
        if query:
            # Split the query into parts (split by spaces)
            name_parts = query.split()

            # Dynamically build the query filters based on the parts
            filter_query = Q()

            for part in name_parts:
                filter_query |= Q(first_name__icontains=part) | Q(middle_initial__icontains=part) | Q(last_name__icontains=part)

            instructors = instructors.filter(filter_query)

        # Debugging: Print the number of instructors fetched
        print(f"Found {instructors.count()} instructors matching the query.")

        # Prepare the response for the search (as JSON for AJAX)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Prepare the list of instructor details to return
            data = [
                {
                    'name': f"{instructor.first_name} {instructor.middle_initial or ''} {instructor.last_name}".strip(),
                    'instructor_id': instructor.instructor_id,
                    'employment_type': instructor.employment_type,
                    'qualified_course': instructor.qualified_course,
                }
                for instructor in instructors
            ]



            return JsonResponse({'results': data})

        # For non-AJAX request, render the instructor list template
        return render(request, 'instructors_frontend/teaching_load.html', {
            'instructors': instructors,
            'filter': filter_type,  # Pass the employment type filter to the template
            'query': query,  # Pass the search query to the template
        })


def instructor_details(request):
    # Get 'id' from query parameters
    instructor_id = request.GET.get('id')

    # Ensure the 'id' is provided and is a valid integer
    if not instructor_id:
        return JsonResponse({'error': 'instructor_id is required'}, status=400)

    try:
        # Convert the instructor_id to an integer (this will raise ValueError if it's not a valid number)
        instructor_id = int(instructor_id)

        # Fetch the instructor record
        instructor = InstructorData.objects.get(instructor_id=instructor_id)

        # Prepare the instructor details to return as JSON
        data = {
            'instructor_id': instructor.instructor_id,
            'name': f"{instructor.first_name} {instructor.middle_initial or ''} {instructor.last_name}".strip(),
            'employment_type': instructor.employment_type,
            'qualified_courses': instructor.qualified_course,
        }

        return JsonResponse(data)

    except ValueError:
        # If 'id' is not a valid integer, return an error
        return JsonResponse({'error': 'Invalid instructor_id format, must be an integer'}, status=400)
    except InstructorData.DoesNotExist:
        # If no instructor is found with the given ID
        return JsonResponse({'error': 'Instructor data not found'}, status=404)

# List instructor courses
def instructor_course_list(request):
    courses = InstructorCourse.objects.all()
    return render(request, 'teaching_load.html', {'courses': courses})

def search_programs(request):
    query = request.GET.get('q', '')
    if query:
        programs = Program.objects.filter(program_name__icontains=query)
    else:
        programs = Program.objects.all()

    program_list = [
        {
            'program_id': program.program_id,
            'program_name': program.program_name,
            'program_code': program.program_code,
        }
        for program in programs
    ]

    return JsonResponse({'programs': program_list})

def program_details(request):
    program_id = request.GET.get('program_id', None)
    if program_id:
        try:
            program = Program.objects.get(program_id=program_id)
            program_data = {
                'program_id': program.program_id,
                'program_name': program.program_name,
                'program_code': program.program_code,
            }
            return JsonResponse({'program': program_data})
        except Program.DoesNotExist:
            return JsonResponse({'error': 'Program not found'}, status=404)
    else:
        return JsonResponse({'error': 'Program ID not provided'}, status=400)

def search_courses(request):
    if request.method == "GET":
        query = request.GET.get('q', '').strip()  # Get the query from request
        courses = InstructorCourse.objects.all()  # Start with all courses

        if query:  # Apply filtering if query exists
            query_parts = query.split()  # Split the query into parts for flexibility
            filter_query = Q()

            # Build the filter dynamically to search in course_code and course_name
            for part in query_parts:
                filter_query |= Q(course_code__icontains=part) | Q(course_name__icontains=part)

            courses = courses.filter(filter_query)  # Apply the filters

        # Prepare the response for suggestions
        data = [
            {
                'course_code': course.course_code,
                'course_name': course.course_name,
                'course_id': course.course_id,
            }
            for course in courses
        ]
        return JsonResponse({'results': data})  # Return the suggestions as JSON

def course_details(request):
    course_id = request.GET.get('id')

    if not course_id:
        return JsonResponse({'error': 'Course ID is required.'}, status=400)

    try:
        course = InstructorCourse.objects.get(course_id=course_id)

        data = {
            'course_id': course.course_id,
            'course_code': course.course_code,
            'course_name': course.course_name,
            'credit_hours': course.credit_hours,
            'semester': course.semester,
        }
        return JsonResponse(data)

    except InstructorCourse.DoesNotExist:
        return JsonResponse({'error': 'Course not found.'}, status=404)

def room_utilization(request):
    return render(request, 'instructors_frontend/room_util.html')  # Update path to match your template location

def search_rooms(request):
    query = request.GET.get('q', '')  # Search query, default to empty string
    building_name = request.GET.get('building', '')  # Optionally filter by building name
    campus_name = request.GET.get('campus', '')  # Optionally filter by campus name

    rooms = Room.objects.all()  # Start with all rooms

    if query:  # Filter by room number if query is provided
        rooms = rooms.filter(room_number__icontains=query)

    if building_name:  # Filter by building name if provided
        rooms = rooms.filter(building__building_name__icontains=building_name)

    if campus_name:  # Filter by campus name if provided
        rooms = rooms.filter(campus__campus_name__icontains=campus_name)

    # Limit to 10 rooms and return relevant data
    rooms_data = [{"room_id": room.room_id, "room_number": room.room_number, "room_type": room.room_type} for room in rooms[:10]]

    return JsonResponse({'rooms': rooms_data})


def room_details(request):
    room_id = request.GET.get('room_id')

    try:
        room = Room.objects.get(room_id=room_id)
        data = {
            'room': {
                'room_number': room.room_number,
                'room_type': room.room_type,
                'building_name': room.building.building_name,
                'campus_name': room.campus.campus_name,
            }
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    
# def schedule_room(request):
#     if request.method == 'POST':
#         room_id = request.POST.get('room')  # Room ID from the hidden input field
#         day = request.POST.get('day')
#         start_time = request.POST.get('start-time')
#         end_time = request.POST.get('end-time')

#         # Error handling for room retrieval
#         try:
#             room = Room.objects.get(id=room_id)
#         except Room.DoesNotExist:
#             # If the room doesn't exist, handle this gracefully (perhaps show an error message)
#             return render(request, 'room_util.html', {'error': 'Room not found'})

#         # Save the schedule to the database
#         room_schedule = RoomSchedule(
#             room=room,
#             day=day,
#             start_time=start_time,
#             end_time=end_time,
#         )

#         try:
#             room_schedule.save()
#         except Exception as e:
#             # Handle unexpected errors while saving
#             return render(request, 'room_util.html', {'error': f'Error saving schedule: {e}'})

#         # Redirect after saving
#         return redirect('schedule_room')  # Redirect to the schedule page or wherever needed

#     return render(request, 'room_util.html')  # Return the schedule page

@csrf_exempt
def save_program_schedule(request):
    if request.method == "POST":

        # Print all request data for debugging
        print(request.POST)

        # Extract and validate required fields
        instructor_name = request.POST.get('instructor_name')
        if not instructor_name:
            return JsonResponse({"error": "Instructor name is required."}, status=400)

        course_code = request.POST.get('course_code')
        if not course_code:
            return JsonResponse({"error": "Course code is required."}, status=400)

        course_name = request.POST.get('course_name', "Untitled Course")
        
        credit_hours = request.POST.get('credit_hours')
        if credit_hours is None or not credit_hours.isdigit():
            return JsonResponse({"error": "Credit hours must be a valid integer."}, status=400)
        credit_hours = int(credit_hours)

        semester = request.POST.get('semester')
        program_name = request.POST.get('program_name')
        program_code = request.POST.get('program_code')
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        building_name = request.POST.get('building_name')   
        campus_name = request.POST.get('campus_name')

        print(f"building_name: {building_name}, campus_name: {campus_name}")  # Debugging line

        # Validate time fields
        start_time_str = request.POST.get('start_time')
        if not start_time_str:
            return JsonResponse({"error": "Start time is required."}, status=400)

        try:
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
        except ValueError:
            return JsonResponse({"error": "Invalid start time format. Use HH:MM AM/PM."}, status=400)

        end_time_str = request.POST.get('end_time')
        if not end_time_str:
            return JsonResponse({"error": "End time is required."}, status=400)

        try:
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return JsonResponse({"error": "Invalid end time format. Use HH:MM AM/PM."}, status=400)

        year_level = request.POST.get('year_level')
        section = request.POST.get('section')
        shift = request.POST.get('shift')

        # Validate day field
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = request.POST.get('day')
        if day not in valid_days:
            return JsonResponse({"error": f"Invalid day '{day}'. Must be one of {', '.join(valid_days)}."}, status=400)
        
        # Check for conflicts in the database
        conflict = ProgramSchedule.objects.filter(
            instructor_name=instructor_name,
            course_code=course_code,
            room_number=room_number,
            day=day,
            start_time=start_time,
            end_time=end_time,
            year_level=year_level,
            section=section,
            shift=shift
        ).exists()

        if conflict:
            return JsonResponse({"error": "Conflict detected! The schedule overlaps with an existing record."}, status=409)

        # Save data to the ProgramSchedule model
        ProgramSchedule.objects.create(
            instructor_name=instructor_name,
            course_code=course_code,
            course_name=course_name,
            credit_hours=credit_hours,
            semester=semester,
            program_name=program_name,
            program_code=program_code,
            room_number=room_number,
            room_type=room_type,
            building_name=building_name,
            campus_name=campus_name,
            day=day,
            start_time=start_time,
            end_time=end_time,
            year_level=year_level,
            section=section,
            shift=shift,
        )

        return JsonResponse({"message": "Program schedule saved successfully!"})
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
