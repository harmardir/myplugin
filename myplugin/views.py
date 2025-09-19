from django.shortcuts import render
from xmodule.modulestore.django import modulestore

def unit_grid(request):
    """
    Display all unit blocks (verticals) for all courses as a grid.
    """

    store = modulestore()
    courses = store.get_courses(read_only=True)
    units = []

    def collect_verticals(block):
        """
        Recursively collect all vertical blocks (units) from a block.
        """
        verticals = []
        if block.category == "vertical":
            verticals.append(block)
        for child in getattr(block, "children", []):
            verticals.extend(collect_verticals(child))
        return verticals

    for course in courses:
        top_blocks = store.get_items(course.id)  # do not pass depth
        for block in top_blocks:
            vertical_blocks = collect_verticals(block)
            for vb in vertical_blocks:
                units.append({
                    "course": str(course.id),
                    "name": getattr(vb, "display_name", "Untitled Unit"),
                    "unit_id": str(vb.location)
                })

    print(f"Total units found: {len(units)}")  # debug
    return render(request, "myplugin/unit_grid.html", {"units": units})





def test_template(request):
    """
    Simple view to test template loading.
    """
    context = {
        "message": "Template is working!"
    }
    return render(request, "myplugin/test_template.html", context)

