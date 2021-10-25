from apps.core.utilities.slugify import slugify


def generate_filename(obj):
    """
    Generate new filename as "First_name-Title" format
    """

    last_name = slugify(obj.last_name)
    if "-" in last_name:
        last_name = last_name.replace("-", "_")

    title = slugify(obj.title)
    if "-" in title:
        title = title.replace("-", "_")
    return f"{last_name.title()}-{title.title()}.{obj.file.name.split('.')[1]}"
