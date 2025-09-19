from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    """
    Display all vertical (unit) blocks for all courses as a grid,
    with URLs to view them in the courseware.
    """
    store = modulestore()
    units = []

    # Get all courses
    courses = store.get_courses(read_only=True)

    for course in courses:
        course_key = course.id  # CourseLocator

        # Get all blocks for this course
        for block_usage in store.get_items(course_key, depth=None):
            # block_usage is BlockUsageLocator
            block = store.get_item(block_usage)

            # Only vertical (unit) blocks
            if block.category == "vertical":
                # Get hierarchy for URL: chapter/sequential/vertical
                sequential = store.get_item(block.parent) if block.parent else None
                chapter = store.get_item(sequential.parent) if sequential and sequential.parent else None

                if chapter and sequential:
                    # Construct courseware path
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

