from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    store = modulestore()
    all_courses = store.get_courses(read_only=True)

    units = []

    for course in all_courses:
        course_key = course.id

        # Just call get_items with the course_key
        blocks = store.get_items(course_key)

        for block in blocks:
            # Only verticals
            if block.category == "vertical":
                parent = getattr(block, 'parent', None)
                parent_id = str(parent) if parent else str(course_key)

                units.append({
                    "course_id": str(course_key),
                    "unit_id": str(block.location),
                    "unit_name": getattr(block, 'display_name', "Untitled Unit"),
                    "parent_id": parent_id,
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

