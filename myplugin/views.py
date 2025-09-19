# myplugin/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    """
    Display all unit blocks (verticals) for all courses as a grid.
    Clicking a unit opens it in an iframe inside its parent sequence.
    """
    store = modulestore()
    all_courses = store.get_courses(read_only=True)

    units = []

    for course in all_courses:
        course_key = course.id
        for block in store.get_items(course_key, depth=0):
            # Only verticals
            if block.category == "vertical":
                # parent is sequence or chapter
                parent = block.parent  # should exist in Teak
                parent_id = str(parent) if parent else str(course_key)
                
                units.append({
                    "course_id": str(course_key),
                    "unit_id": str(block.location),
                    "unit_name": block.display_name or "Untitled Unit",
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

