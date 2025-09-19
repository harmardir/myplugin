import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.views import View

LMS_BASE_URL = getattr(settings, "LMS_BASE_URL", "http://local.openedx.io:8000")

class UnitListView(View):
    def get(self, request, course_id):
        api_url = f"{LMS_BASE_URL}/api/courses/v2/blocks/"
        params = {
            "course_id": course_id,
            "depth": "all",
            "requested_fields": "display_name,type",
            "block_types_filter": "vertical",
        }
        cookies = request.COOKIES
        resp = requests.get(api_url, params=params, cookies=cookies)
        try:
            data = resp.json()
        except Exception as e:
            # For debugging: print or log the actual error
            error_details = f"Failed to decode JSON. Status: {resp.status_code}, Response: {resp.text}"
            print(error_details)
            return HttpResponseServerError(f"LMS API error: {error_details}")
        units = [
            {"id": key, "display_name": block.get("display_name", key)}
            for key, block in data.get("blocks", {}).items()
        ]
        return render(request, "myplugin/unit_list.html", {"units": units, "course_id": course_id})