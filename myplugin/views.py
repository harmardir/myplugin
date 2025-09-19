from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    """
    Display all vertical units for all courses as a grid.
    Clicking a unit loads it below in an iframe.
    """
    store = modulestore()
    units = []

    courses = store.get_courses(read_only=True)

    for course in courses:
        course_key = course.id

        # ⚡ get_items() returns block objects directly in Teak
        for block in store.get_items(course_key):
            if block.category == "vertical":
                # Traverse up to sequential and chapter
                sequential = getattr(block, 'parent', None)
                chapter = getattr(sequential, 'parent', None) if sequential else None

                if chapter and sequential:
                    # Build URL path for LMS courseware
                    path = f"{chapter.location}/{sequential.location}/{block.location}"
                    units.append({
                        "course": str(course_key),
                        "name": getattr(block, 'display_name', 'Untitled Unit'),
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

