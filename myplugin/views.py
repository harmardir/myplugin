from common.djangoapps.edxmako.shortcuts import render_to_response
from xmodule.modulestore.django import modulestore
from lms.djangoapps.courseware.module_render import get_module_by_usage_id
from openedx.core.djangoapps.plugin_api.views import get_course_key

def list_units(request):
    store = modulestore()
    courses_data = []

    all_courses = store.get_courses()
    for course in all_courses:
        course_info = {
            "id": str(course.id),
            "display_name": getattr(course, "display_name", "Unnamed Course"),
            "units": []
        }

        for block in store.get_items(course.id):
            if block.location.category == "vertical":
                try:
                    # Render the XBlock fragment for this unit
                    module = get_module_by_usage_id(
                        request, str(course.id), str(block.location)
                    )
                    fragment = module.render("student_view", context={})

                    course_info["units"].append({
                        "id": str(block.location),
                        "display_name": getattr(block, "display_name", "Unnamed Unit"),
                        "html": fragment.content,
                        "js": fragment.js(),
                        "css": fragment.css(),
                    })
                except Exception as e:
                    # fallback if render fails
                    course_info["units"].append({
                        "id": str(block.location),
                        "display_name": getattr(block, "display_name", "Unnamed Unit"),
                        "html": f"<p>Error rendering unit: {e}</p>",
                        "js": "",
                        "css": "",
                    })

        courses_data.append(course_info)

    context = {"courses": courses_data}
    return render_to_response("myplugin/units.html", context)
