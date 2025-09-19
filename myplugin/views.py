from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    store = modulestore()
    units = []

    # ⚡ Use get_course_keys() instead of get_courses()
    for course_key in store.get_course_keys():
        for locator in store.get_items(course_key):
            block = store.get_item(locator)
            if block.category == "vertical":
                sequential = store.get_item(block.parent) if block.parent else None
                chapter = store.get_item(sequential.parent) if sequential and sequential.parent else None

                if chapter and sequential:
                    path = f"{chapter.location}/{sequential.location}/{block.location}"
                    units.append({
                        "course": str(course_key),  # for URLs
                        "name": block.display_name or "Untitled Unit",
                        "url": f"/courses/{str(course_key)}/courseware/{path}/"
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

