import io
import math
import sys

import PIL.Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def сompressImage(image, target=5120000):
    """Сохраняем изображение с оптимальным качеством не привышающим "target" в байтах."""
    name = str(image).split(".")[0]
    img = PIL.Image.open(image)
    # минимальное и максимальное качество
    Qmin, Qmax = 25, 96
    # находим оптимально-допустимое качество
    Qacc = -1
    while Qmin <= Qmax:
        middle = math.floor((Qmin + Qmax) / 2)
        # получаем размер изображения
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", optimize=True, quality=middle, progressive=True)
        size = buffer.getbuffer().nbytes
        if size <= target:
            Qmin = middle + 1
        elif size > target:
            Qmax = middle - 1
    # записываем с определившимся качеством
    if Qacc > -1:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", optimize=True, quality=Qacc, progressive=True)
        new_image = InMemoryUploadedFile(
            buffer, "ImageField", "%s.jpg" % name, "image/jpeg", sys.getsizeof(buffer), None
        )
        return new_image
    else:
        print("ERROR: No acceptble quality factor found")
