# myplugin/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import CourseKey

def unit_grid(request):
    """
    Display all unit blocks (verticals) for all courses as a grid.
    """
    store = modulestore()
    all_courses = store.get_courses(read_only=True)

    units = []

    for course in all_courses:
        course_key = CourseKey.from_string(str(course.id))
        try:
            blocks = store.get_items(course_key)  # <- No depth argument
        except Exception as e:
            print(f"Failed to get blocks for course {course.id}: {e}")
            continue

        for block in blocks:
            if getattr(block, "category", None) == "vertical":
                # Use student_view_url if available, else fallback to usage_key
                usage_key = getattr(block, "usage_key", None)
                display_name = getattr(block, "display_name", "Untitled Unit")
                units.append({
                    "course": str(course.id),
                    "unit_id": str(usage_key),
                    "display_name": display_name,
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

