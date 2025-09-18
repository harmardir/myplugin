from django.shortcuts import render
from opaque_keys.edx.keys import CourseKey
from student.models import CourseEnrollment
from xmodule.modulestore.django import modulestore

def courses_and_units_view(request):
    """
    Fetch all courses the current user is enrolled in and their sequential units,
    then render them with the Mako template.
    """
    user = request.user
    courses = []

    # Get all enrolled courses for the current user
    enrolled_courses = CourseEnrollment.objects.filter(user=user)

    for enrollment in enrolled_courses:
        course_id = enrollment.course_id
        course_key = CourseKey.from_string(course_id)
        course = modulestore().get_course(course_key)

        # Collect all sequential units in the course
        units = []
        for block in course.get_children():
            if block.category == "sequential":
                units.append({
                    "id": str(block.location),
                    "display_name": block.display_name,
                    "url": f"/myplugin/unit/{block.location}/",  # placeholder for unit view
                })

        courses.append({
            "id": course_id,
            "display_name": course.display_name,
            "units": units,
        })

    return render(request, "myplugin/courses_and_units.html", {"courses": courses})
