from urllib.parse import quote
from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    store = modulestore()
    all_courses = store.get_courses()

    units = []
    for course in all_courses:
        for block in store.get_items(course.id):
            if block.location.category == 'vertical':
                units.append({
                    "course": str(course.id),
                    "unit_id": str(block.location),        # display
                    "unit_url": quote(str(block.location)), # safe for URLs
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

