from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore
from common.djangoapps.edxmako.shortcuts import render_to_response


@login_required
def units_list(request):
    """
    Show all courses and their units (vertical blocks) in a grid.
    """
    store = modulestore()
    courses = []

    # Loop through all courses
    for course in store.get_courses():
        course_dict = {
            "id": str(course.id),
            "display_name": getattr(course, "display_name", str(course.id)),
            "units": []
        }

        # Collect unit blocks (category == 'vertical')
        for block in store.get_items(course.id):
            if getattr(block.location, "category", None) == "vertical":
                course_dict["units"].append({
                    "id": str(block.location),
                    "display_name": getattr(block, "display_name", str(block.location)),
                })

        courses.append(course_dict)

    context = {"courses": courses}
    return render_to_response("myplugin/units.html", context)


@login_required
def render_unit(request, usage_key_str):
    """
    Render a single unit page in LMS chrome.
    """
    store = modulestore()
    try:
        usage_key = UsageKey.from_string(usage_key_str)
        block = store.get_item(usage_key)
    except Exception:
        raise Http404("Unit not found")

    context = {
        "unit_id": str(block.location),
        "unit_display_name": getattr(block, "display_name", str(block.location)),
        "block": block,
    }

    return render_to_response("myplugin/unit_detail.html", context)
