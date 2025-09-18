from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.test import APIRequestFactory
from lms.djangoapps.courseware_api.views import CourseViewSet, BlocksViewSet


def courses_and_units_view(request):
    """
    Fetch all courses and their units using the Courseware API,
    then render with a Mako template.
    """
    factory = APIRequestFactory()

    # Call Course API to get all enrolled courses
    course_api_req = factory.get("/api/courseware/course/")
    course_response = CourseViewSet.as_view({"get": "list"})(course_api_req)

    courses = []
    for course in course_response.data.get("results", []):
        course_id = course["id"]

        # Call Blocks API to get blocks for this course
        blocks_req = factory.get(f"/api/courseware/blocks/?course_id={course_id}&all_blocks=true")
        blocks_response = BlocksViewSet.as_view({"get": "list"})(blocks_req)

        blocks_data = blocks_response.data.get("blocks", {})

        # Filter units (sequences typically)
        units = [
            {
                "id": blk_id,
                "display_name": blk.get("display_name", "Untitled"),
                "url": f"/myplugin/unit/{blk_id}/",
            }
            for blk_id, blk in blocks_data.items()
            if blk.get("type") == "sequential"
        ]

        courses.append({
            "id": course_id,
            "display_name": course["display"],
            "units": units,
        })

    context = {"courses": courses}

    return render_to_response(
        "myplugin/courses_and_units.html",
        context,
        context_instance=RequestContext(request),
    )
