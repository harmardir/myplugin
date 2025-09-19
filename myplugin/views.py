from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    store = modulestore()
    units = []

    # Get all courses
    courses = store.get_courses(read_only=True)

    for course in courses:
        course_key = course.id  # CourseLocator

        # ⚡ Remove 'depth' argument
        for block_usage in store.get_items(course_key):
            block = store.get_item(block_usage)

            if block.category == "vertical":
                # Try to get parent sequential and chapter
                sequential = store.get_item(block.parent) if block.parent else None
                chapter = store.get_item(sequential.parent) if sequential and sequential.parent else None

                if chapter and sequential:
                    path = f"{chapter.location}/{sequential.location}/{block.location}"
                    units.append({
                        "course": str(course_key),
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

