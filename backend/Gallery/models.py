import os

from PIL import Image
from django.db import models

from django.utils import timezone

# функция генерации пути
def get_path_upload_image(file):

    time = timezone.now().strftime("%Y-%m-%d")
    # находим расширение
    end_extention = file.split('.')[1]
    # находим имя файла
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    file_name = head + '_' + timezone.now().strftime("%Y-%m-%d") + '.' + end_extention
    return os.path.join('photos', '{}', '{}').format(time, file_name)

class Photo(models.Model):
    # Фото
    name = models.CharField("Имя", max_length=50)
    # для image генерирует путь(user, date)
    # создавать миниатюры, ограничить вес фото, размер
    image = models.ImageField("Фото", upload_to="Gallery/")
    created = models.DateTimeField("Дата создания картинки", auto_now_add=True)
    slug = models.SlugField("url", max_length=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.image.name = get_path_upload_image(self.image.name)
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

class Gallery(models.Model):
    # Галерея картинок
    name = models.CharField("Имя", max_length=50)
    photos = models.ManyToManyField(Photo, verbose_name="Фото")
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    slug = models.SlugField("url", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереии"
