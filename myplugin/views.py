from django.shortcuts import render
from xmodule.modulestore.django import modulestore
from urllib.parse import quote

def unit_grid(request):
    store = modulestore()
    units = []

    for course in store.get_courses():
        for block in store.get_items(course.id):
            if block.location.category == "vertical":
                sequential = block.parent
                chapter = sequential.parent if sequential else None
                if chapter and sequential:
                    path = f"{chapter.location}/{sequential.location}/{block.location}"
                    units.append({
                        "course": str(course.id),
                        "name": block.display_name or "Untitled Unit",
                        "url": f"/courses/{course.id}/courseware/{path}/"
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

