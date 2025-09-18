from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from xmodule.modulestore.django import modulestore

@login_required
def units_list(request):
    """
    Display a list of all courses and their units (vertical blocks).
    """
    store = modulestore()
    courses = []

    for course in store.get_courses():
        course_dict = {
            "id": str(course.id),  # UsageKey or CourseKey as string
            "display_name": getattr(course, "display_name", str(course.id)),
            "units": []
        }
        # Find all vertical (unit) blocks in the course
        for block in store.get_items(course.id):
            if getattr(block.location, "category", None) == "vertical":
                unit_dict = {
                    "id": str(block.location),  # UsageKey as string
                    "display_name": getattr(block, "display_name", str(block.location)),
                }
                course_dict["units"].append(unit_dict)
        courses.append(course_dict)

    return render(request, "myplugin/units.html", {"courses": courses})