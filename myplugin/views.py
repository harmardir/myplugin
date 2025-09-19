# myplugin/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import CourseKey

def unit_grid(request):
    """
    Display all vertical (unit) blocks for all courses as a grid.
    """
    store = modulestore()
    all_courses = store.get_courses(read_only=True)
    units = []

    def traverse_blocks(block):
        """Recursively traverse children to find verticals."""
        if getattr(block, "category", None) == "vertical":
            usage_key = getattr(block, "usage_key", None)
            units.append({
                "course": str(course.id),
                "unit_id": str(usage_key),
                "display_name": getattr(block, "display_name", "Untitled Unit"),
            })
        # Recursively check children
        children = getattr(block, "children", []) or []
        for child_locator in children:
            try:
                child_block = store.get_item(child_locator)
                traverse_blocks(child_block)
            except Exception as e:
                print(f"Failed to load child block {child_locator}: {e}")

    for course in all_courses:
        course_key = CourseKey.from_string(str(course.id))
        try:
            top_blocks = store.get_items(course_key)
        except Exception as e:
            print(f"Failed to get top-level blocks for course {course.id}: {e}")
            continue

        for block in top_blocks:
            traverse_blocks(block)

    return render(request, "myplugin/unit_grid.html", {"units": units})







def test_template(request):
    """
    Simple view to test template loading.
    """
    context = {
        "message": "Template is working!"
    }
    return render(request, "myplugin/test_template.html", context)

