from common.djangoapps.edxmako.shortcuts import render_to_response
from xmodule.modulestore.django import modulestore

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
