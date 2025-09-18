from django.urls import reverse
from common.djangoapps.edxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from xmodule.modulestore.django import modulestore

@login_required
def units_list(request):
    store = modulestore()
    courses = []

    for course in store.get_courses():
        course_dict = {
            "id": str(course.id),
            "display_name": getattr(course, "display_name", str(course.id)),
            "units": []
        }
        for block in store.get_items(course.id):
            if getattr(block.location, "category", None) == "vertical":
                # Generate deep-link to courseware unit
                unit_url = reverse(
                    "courseware.views.index",
                    args=[str(course.id), str(block.location)]
                )
                course_dict["units"].append({
                    "id": str(block.location),
                    "display_name": getattr(block, "display_name", str(block.location)),
                    "url": unit_url,
                })
        courses.append(course_dict)

    return render_to_response("myplugin/units.html", {"courses": courses})
