from django.core.exceptions import ValidationError


def images_in_block_changed(sender, **kwargs):
    print("here")
    if kwargs["instance"].images_in_block.count() > 8:
        raise ValidationError("You can't assign more than eight images")
