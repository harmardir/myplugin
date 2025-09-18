from django.contrib.auth.decorators import login_required
from django.http import Http404
from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore
from common.djangoapps.edxmako.shortcuts import render_to_response

@login_required
def render_unit(request, usage_key_str):
    """
    Render a single unit block inside an LMS page with Mako template.
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
