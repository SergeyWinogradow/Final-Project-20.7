from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

from PIL import Image
from django.db import models
import os
from django.utils import timezone

# функция генерации пути
def get_path_upload_image(instance, file):

    time = timezone.now().strftime("%Y-%m-%d")
    end_extention = file.split('.')[1]
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    file_name = head + '_' + time + '.' + end_extention
    return os.path.join('profile_pics', 'user_{0}, {1}').format(instance.user.id, file_name)


class Profile(models.Model):
    # модель профиля пользователя
    user = models.OneToOneField(User, verbose_name="пользователь", on_delete=models.CASCADE)
    avatar = models.ImageField("Аватар", upload_to="profiles/", blank=True, null=True)
    nike = models.CharField("НикНейм", max_length=100, null=True, blank=True)
    email_two = models.EmailField("доп. email")
    phone = models.CharField("Телефон", max_length=25)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50, blank=True, null=True)
    #follow = models.ManyToManyField(User, verbose_name="Подписчики", related_name="follow_user")
    slug = models.SlugField("url", max_length=50, default='')

    # def __str__(self):
    #     return self.first_name

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
       verbose_name = "Профиль"
       verbose_name_plural = "Профили"

    @property
    def get_avatar_url(self):
        if self.avatar:
            return '/media/{}'.format(self.user)
        else:
            return 'static/img/default.png'

    @property
    def get_followers(self):
        if self.follow:
            return self.follow.all()
        else:
            return 'нет подписчиков'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     # Создание профиля пользователя при регистрации
#     if created:
#         Profile.object.create(user=instance)

@receiver
def create_user_profile(sender, instance, **kwargs):
    instance.profiles.save()