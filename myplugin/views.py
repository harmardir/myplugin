# myplugin/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import CourseKey

def unit_grid(request):
    """
    Display all unit blocks (verticals) for all courses as a grid
    with clickable iframes showing actual LMS content.
    """
    store = modulestore()
    all_courses = store.get_courses(read_only=True)

    units = []
    for course in all_courses:
        # Get course key object
        course_key = CourseKey.from_string(str(course.id))
        # Get all blocks in course
        blocks = store.get_items(course_key, depth=None)

        for block in blocks:
            if block.category == "vertical":
                # Get LMS URL for the unit
                student_url = getattr(block, "student_view_url", None)
                if not student_url:
                    continue

                units.append({
                    "course_name": getattr(course, "display_name", str(course.id)),
                    "unit_name": getattr(block, "display_name", "Untitled Unit"),
                    "unit_url": student_url  # correct LMS URL
                })

    return render(request, "myplugin/unit_grid.html", {"units": units})





def test_template(request):
    """
    Simple view to test template loading.
    """
    context = {
        "message": "Template is working!"
    }
    return render(request, "myplugin/test_template.html", context)

