import sys
from io import BytesIO

import PIL.Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def сompressImage(image):
    try:
        name = str(image).split(".")[0]
        img = PIL.Image.open(image)
        output = BytesIO()
        img.thumbnail((400, 400))
        img.save(output, format="JPEG", optimize=True, quality=85, progressive=True)
        new_image = InMemoryUploadedFile(
            output, "ImageField", "%s.jpg" % name, "image/jpeg", sys.getsizeof(output), None
        )
        return new_image
    except Exception as e:
        return e
