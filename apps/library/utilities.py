from apps.info.models import Festival


def generate_class_name_path(instance, filename):
    festival = Festival.objects.last()
    return f"{instance.__class__.__name__}/{festival.year}/{filename}"


def get_slug_name(instance):
    return instance.person.last_name
