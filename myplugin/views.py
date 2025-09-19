from django.shortcuts import render
from xmodule.modulestore.django import modulestore
from urllib.parse import quote

def unit_grid(request):
    """
    Display all vertical units for a course as a grid with iframe links to LMS courseware.
    """
    store = modulestore()
    course_key = "course-v1:OpenedX+DemoX+DemoCourse"
    course = store.get_course(course_key)

    units = []

    for block in store.get_items(course.id):
        # Only vertical units
        if block.location.category == "vertical":
            # Get the parent sequential and chapter to build LMS path
            sequential = block.parent
            chapter = sequential.parent if sequential else None

            if chapter and sequential:
                # Build courseware path
                courseware_path = f"{chapter.location}/{sequential.location}/{block.location}"
                units.append({
                    "name": block.display_name or "Untitled Unit",
                    "url": f"/courses/{course.id}/courseware/{courseware_path}/",
                })

    context = {"units": units, "course_key": course.id}
    return render(request, "myplugin/unit_grid.html", context)


def test_template(request):
    """
    Simple view to test template loading.
    """
    context = {
        "message": "Template is working!"
    }
    return render(request, "myplugin/test_template.html", context)

