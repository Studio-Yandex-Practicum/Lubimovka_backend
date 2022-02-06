from datetime import datetime as dt


def get_festival_year():
    if 7 <= dt.now().month <= 12:
        return dt.now().year + 1
    return dt.now().year


def generate_class_name_path(instance, filename):
    festival_year = get_festival_year()
    return f"{instance.__class__.__name__}/{festival_year}/{filename}"
