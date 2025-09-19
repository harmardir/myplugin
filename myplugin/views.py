from django.shortcuts import render
from django.views import View
from openedx.core.djangoapps.content.block_structure.api import get_course_blocks
from opaque_keys.edx.keys import CourseKey
import requests
from django.conf import settings
from django.http import HttpResponse

class UnitListView(View):
    def get(self, request, course_id):
        user = request.user
        course_key = CourseKey.from_string(course_id)
        blocks = get_course_blocks(user, course_key)
        unit_blocks = [
            {
                "id": str(block_key),
                "display_name": blocks.get_xblock_field(block_key, 'display_name')
            }
            for block_key in blocks.get_all_block_keys()
            if blocks.get_xblock_field(block_key, 'category') == 'vertical'
        ]
        return render(request, "myplugin/unit_list.html", {"units": unit_blocks, "course_id": course_id})



LMS_BASE_URL = getattr(settings, "LMS_BASE_URL", "http://local.openedx.io:8000")

class UnitContentView(View):
    def get(self, request, unit_id):
        # Proxy the LMS unit content endpoint, using the user's session
        url = f"{LMS_BASE_URL}/xblock/{unit_id}"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        cookies = request.COOKIES
        params = {"view": "student"}
        resp = requests.get(url, params=params, cookies=cookies, headers=headers)
        return HttpResponse(resp.text)