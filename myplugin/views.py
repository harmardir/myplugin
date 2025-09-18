import requests
from django.conf import settings
from django.shortcuts import render

def courses_and_units_view(request):
    lms_base = "http://localhost:8000"  # LMS domain in dev
    api_url = f"{lms_base}/api/courseware/courses/"  # list courses

    # Use session cookies from request if needed for auth
    resp = requests.get(api_url, cookies=request.COOKIES)
    courses_data = resp.json().get("results", [])

    # For each course, fetch blocks
    for course in courses_data:
        course_id = course["id"]
        blocks_url = f"{lms_base}/api/courseware/blocks/?course_id={course_id}&all_blocks=true"
        blocks_resp = requests.get(blocks_url, cookies=request.COOKIES)
        blocks_data = blocks_resp.json().get("blocks", {})
        course["units"] = [
            {"id": blk_id, "display_name": blk.get("display_name", "Untitled")}
            for blk_id, blk in blocks_data.items()
            if blk.get("type") == "sequential"
        ]

    context = {"courses": courses_data}
    return render(request, "myplugin/courses_and_units.html", context)
