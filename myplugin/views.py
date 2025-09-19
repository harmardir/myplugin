# myplugin/views.py
from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    """
    Display all unit blocks (verticals) for all courses as a grid (Teak-safe).
    """
    store = modulestore()
    courses = store.get_courses(read_only=True)

    units = []

    for course in courses:
        # Get top-level blocks (course tree)
        try:
            blocks = store.get_items(course.id)  # do not pass depth
        except Exception as e:
            print(f"Error loading blocks for course {course.id}: {e}")
            continue

        for b in blocks:
            # Determine the actual block object and usage key
            if hasattr(b, "location"):
                block_obj = b
                usage_key = str(b.location)
            else:
                # might be a locator
                try:
                    block_obj = store.get_item(b)
                    usage_key = str(block_obj.location)
                except Exception as e:
                    print(f"Cannot get item for {b}: {e}")
                    continue

            # Only include unit/vertical blocks
            if getattr(block_obj, "category", None) == "vertical":
                units.append({
                    "course": str(course.id),
                    "unit_id": usage_key,
                    "display_name": getattr(block_obj, "display_name", "Untitled Unit")
                })

    return render(request, "myplugin/unit_grid.html", {"units": units})






def test_template(request):
    """
    Simple view to test template loading.
    """
    context = {
        "message": "Template is working!"
    }
    return render(request, "myplugin/test_template.html", context)

