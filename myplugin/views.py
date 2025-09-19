import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

LMS_BASE_URL = getattr(settings, "LMS_BASE_URL", "http://local.openedx.io:8000/")

class UnitListView(View):
    def get(self, request, course_id):
        # Fetch all blocks for the course
        api_url = f"{LMS_BASE_URL}/api/courses/v2/blocks/"
        params = {
            "course_id": course_id,
            "depth": "all",
            "requested_fields": "display_name,type",
            "block_types_filter": "vertical",  # Only units
        }
        cookies = request.COOKIES  # forward user cookies for auth
        resp = requests.get(api_url, params=params, cookies=cookies)
        data = resp.json()
        # units = [block for block in data['blocks'].values() if block['type'] == 'vertical']
        # Blocks are dicts keyed by usage key
        units = [
            {"id": key, "display_name": block.get("display_name", key)}
            for key, block in data.get("blocks", {}).items()
        ]
        return render(request, "mycourse/unit_list.html", {"units": units, "course_id": course_id})

class UnitContentView(View):
    def get(self, request, unit_id):
        # Fetch unit HTML from the LMS xblock endpoint
        url = f"{LMS_BASE_URL}/xblock/{unit_id}"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        cookies = request.COOKIES
        # Forward query params if present (view, etc.)
        params = {"view": "student"}
        resp = requests.get(url, params=params, cookies=cookies, headers=headers)
        # Return HTML fragment (not JSON)
        return HttpResponse(resp.text)