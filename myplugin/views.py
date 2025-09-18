from django.http import HttpResponse
from xmodule.modulestore.django import modulestore
from xmodule.x_module import XModuleDescriptor
from opaque_keys.edx.keys import UsageKey

def render_unit(request, usage_key_str):
    """
    Render a single unit (vertical block) as plain HTML.
    """
    store = modulestore()
    usage_key = UsageKey.from_string(usage_key_str)

    block = store.get_item(usage_key)

    # Blocks have a render method, but need a runtime.
    # This is simplified — in production you’d use LMS runtimes.
    if hasattr(block, 'render'):
        fragment = block.render('student_view')
        return HttpResponse(fragment.content)

    return HttpResponse("<p>Cannot render this block type.</p>")
