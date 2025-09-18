from django.contrib.auth.decorators import login_required
from django.http import Http404
from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore
from common.djangoapps.edxmako.shortcuts import render_to_response

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
                unit_dict = {
                    "id": str(block.location),
                    "display_name": getattr(block, "display_name", str(block.location)),
                    "url": reverse("myplugin:render_unit", args=[str(block.location)]),  # ✅ build URL here
                }
                course_dict["units"].append(unit_dict)
        courses.append(course_dict)

    return render_to_response("myplugin/units.html", {"courses": courses})

@login_required
def render_unit(request, usage_key_str):
    """
    Render a unit (vertical block) using legacy courseware rendering.
    """
    usage_key = UsageKey.from_string(usage_key_str)
    store = modulestore()
    unit = get_object_or_404(store, usage_key)

    # Use the old courseware view helper
    from lms.djangoapps.courseware.views.views import unit as courseware_unit_view

    # Call the legacy unit renderer
    return courseware_unit_view(request, usage_key.course_key, usage_key)
