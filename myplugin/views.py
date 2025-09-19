# myapp/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    """
    Display all unit blocks (verticals) for all courses as a grid.
    """
    store = modulestore()
    all_courses = store.get_courses()

    units = []
    for course in all_courses:
        for block in store.get_items(course.id):
            if block.location.category == 'vertical':
                units.append({
                    "course": str(course.id),
                    "unit_id": str(block.location),  # usage key
                })

    return render(request, "myplugin/unit_grid.html", {"units": units})
