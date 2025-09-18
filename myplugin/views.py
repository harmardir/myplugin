from django.http import HttpResponse, JsonResponse
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import UsageKey
from xmodule.runtime import Runtime

def render_unit(request, usage_key_str):
    """
    Render a single unit as full HTML page (for fallback / direct link).
    """
    store = modulestore()
    usage_key = UsageKey.from_string(usage_key_str)
    block = store.get_item(usage_key)

    runtime = Runtime(user=request.user, store=store, services={})

    try:
        fragment = block.render(runtime, 'student_view')
        return HttpResponse(fragment.content)
    except Exception as e:
        return HttpResponse(f"<p>Error rendering block: {e}</p>")


def render_unit_json(request, usage_key_str):
    """
    Return unit content as JSON to load inline via AJAX.
    """
    store = modulestore()
    usage_key = UsageKey.from_string(usage_key_str)
    block = store.get_item(usage_key)

    runtime = Runtime(user=request.user, store=store, services={})

    try:
        fragment = block.render(runtime, 'student_view')
        return JsonResponse({"html": fragment.content})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
