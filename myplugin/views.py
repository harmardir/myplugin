# myapp/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore

from common.djangoapps.edxmako.shortcuts import render_to_response
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


def test_template(request):
    """
    Simple view to test template loading.
    """
    context = {
        "message": "Template is working!"
    }
    return render(request, "myplugin/test_template.html", context)



def hello_world(request):
    context = {"message": "Hello from MyPlugin (HTML)!"}
    return render(request, "myplugin/hello.html", context)




def list_units(request):
    store = modulestore()
    courses_data = []

    # Get all courses
    all_courses = store.get_courses()
    for course in all_courses:
        course_info = {
            "id": str(course.id),
            "display_name": getattr(course, "display_name", "Unnamed Course"),
            "units": []
        }

        # Collect unit blocks
        for block in store.get_items(course.id):
            if block.location.category == "vertical":
                course_info["units"].append({
                    "id": str(block.location),
                    "display_name": getattr(block, "display_name", "Unnamed Unit"),
                })

        courses_data.append(course_info)

    context = {"courses": courses_data}

    # Renders your Mako template
    return render_to_response("myplugin/units.html", context)
