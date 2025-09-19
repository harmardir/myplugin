from django.shortcuts import render
from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    store = modulestore()
    units = []

    # get_courses() returns CourseLocator objects
    for course in store.get_courses():
        # Pass course (CourseLocator) directly to get_items()
        for locator in store.get_items(course):
            block = store.get_item(locator)
            if block.category == "vertical":
                # Get parent sequential and chapter safely
                sequential = store.get_item(block.parent) if block.parent else None
                chapter = store.get_item(sequential.parent) if sequential and sequential.parent else None

                if chapter and sequential:
                    path = f"{chapter.location}/{sequential.location}/{block.location}"
                    units.append({
                        "course": str(course),  # course key as string for URLs
                        "name": block.display_name or "Untitled Unit",
                        "url": f"/courses/{str(course)}/courseware/{path}/"
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

