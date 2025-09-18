from django.urls import reverse
from xmodule.modulestore.django import modulestore
from common.djangoapps.edxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


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
                # Deep link into courseware
                courseware_url = reverse(
                    "courseware",
                    args=[str(course.id)]
                ) + f"?activate_block_id={str(block.location)}"

                unit_dict = {
                    "id": str(block.location),
                    "display_name": getattr(block, "display_name", str(block.location)),
                    "url": courseware_url,
                }
                course_dict["units"].append(unit_dict)

        courses.append(course_dict)

    context = {"courses": courses}
    return render_to_response("myplugin/units.html", context)
