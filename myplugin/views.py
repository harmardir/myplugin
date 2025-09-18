from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from opaque_keys.edx.keys import UsageKey
from openedx.core.djangoapps.xblock.views import student_view

@login_required
def render_unit(request, usage_key_str):
    """
    Renders the XBlock unit using the built-in Open edX student_view,
    which handles runtime and permissions correctly.
    """
    # student_view expects `usage_key_string` as positional argument
    return student_view(request, usage_key_str)

@login_required
def render_unit_json(request, usage_key_str):
    """
    Renders the XBlock unit as HTML and returns it in JSON.
    """
    # Reuse the student_view, capture the rendered content
    response = student_view(request, usage_key_str)
    if response.status_code == 200:
        # If student_view returns an HttpResponse with content, wrap it
        return JsonResponse({"html": response.content.decode()})
    else:
        return JsonResponse({"error": response.content.decode()}, status=response.status_code)