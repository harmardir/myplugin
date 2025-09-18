from django.shortcuts import render
from rest_framework.test import APIRequestFactory
from lms.djangoapps.courseware_api.views import CourseViewSet, BlocksViewSet


def courses_and_units_view(request):
    factory = APIRequestFactory()

    # Call Course API
    course_api_req = factory.get("/api/courseware/course/")
    course_response = CourseViewSet.as_view({"get": "list"})(course_api_req)

    courses = []
    for course in course_response.data.get("results", []):
        course_id = course["id"]

        # Call Blocks API
        blocks_req = factory.get(f"/api/courseware/blocks/?course_id={course_id}&all_blocks=true")
        blocks_response = BlocksViewSet.as_view({"get": "list"})(blocks_req)

        blocks_data = blocks_response.data.get("blocks", {})

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
    return render(request, "myplugin/courses_and_units.html", context)
