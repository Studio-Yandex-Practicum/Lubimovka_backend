def path_by_app_label_and_class_name(instance, filename):
    """Return path in format /`app_label`/`class_name`s/`filename`."""
    app_label = instance._meta.app_label
    class_name_lower = instance.__class__.__name__.lower()
    path = f"images/{app_label}/{class_name_lower}s/{filename}"
    return path


def path_by_media_app_label_and_class_name(instance, filename):
    """Return path in format media/`class_name`s/`filename`."""
    class_name_lower = instance.__class__.__name__.lower()
    path = f"media/{class_name_lower}s/{filename}"
    return path
