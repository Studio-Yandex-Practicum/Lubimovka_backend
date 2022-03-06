import io
import math
import sys

import PIL.Image
from django.core.files.uploadedfile import InMemoryUploadedFile

QUALITY_MIN = 25
QUALITY_MAX = 96
TARGET = 5120000


def save_and_check_size(img, quality):
    """Сохраняет и возвращает размер файла и буфер."""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", optimize=True, quality=quality, progressive=True)
    size = buffer.getbuffer().nbytes
    return size, buffer


def сompressImage(image, target=TARGET):
    """Сохраняем изображение с оптимальным качеством не привышающим "target" в байтах."""
    try:
        name = str(image).split(".")[0]
        img = PIL.Image.open(image)
        # пробуем сохранить картинку без сжимания
        size_without_compress = save_and_check_size(img, 100)
        if size_without_compress[0] <= target:
            buffer = size_without_compress[1]
            new_image = InMemoryUploadedFile(
                buffer, "ImageField", "%s.jpg" % name, "image/jpeg", sys.getsizeof(buffer), None
            )
            return new_image
        # если размер файла превышает target
        # устанавливаем минимальное и максимальное качество
        quality_min, quality_max = QUALITY_MIN, QUALITY_MAX
        # находим оптимально-допустимое качество
        quality_acceptable = -1
        while quality_min <= quality_max:
            middle = math.floor((quality_min + quality_max) / 2)
            # получаем размер изображения
            size = save_and_check_size(img, middle)[0]
            if size <= target:
                quality_acceptable = middle
                quality_min = middle + 1
            elif size > target:
                quality_max = middle - 1
        # записываем с определившимся качеством
        if quality_acceptable > -1:
            save_after_compress = save_and_check_size(img, quality_acceptable)
            buffer = save_after_compress[1]
            new_image = InMemoryUploadedFile(
                buffer, "ImageField", "%s.jpg" % name, "image/jpeg", sys.getsizeof(buffer), None
            )
            return new_image
        else:
            raise Exception("ERROR: No acceptable quality factor found")
    except Exception as e:
        return f"Проблема с загрузкой изображения, ошибка:{e}"
