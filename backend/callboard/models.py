from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django_filters import FilterSet, DateFilter, ModelChoiceFilter, ModelMultipleChoiceFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import send_mail
from django.utils.html import strip_tags

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class Category(MPTTModel):
    """Категории объявлений"""
    name = models.CharField("Имя", max_length=50, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родитель"
    )
    slug = models.SlugField("url", max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = "Категории"


class FilterAdvert(models.Model):
    """Фильтры"""
    name = models.CharField("Имя", max_length=50, unique=True)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"
        ordering = ["id"]

class DateAdvert(models.Model):
    """Срок для объявления"""
    name = models.CharField("Имя", max_length=50, unique=True)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Срок"
        verbose_name_plural = "Сроки"
        ordering = ["id"]


class Advert(models.Model):
    """Объявления"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    filters = models.ForeignKey(FilterAdvert, verbose_name="Фильтр", on_delete=models.CASCADE)
    date = models.ForeignKey(DateAdvert, verbose_name="Срок", on_delete=models.CASCADE)
    subject = models.CharField("Тема", max_length=200)
    description = models.TextField("Объявление", max_length=10000)
    #  загрузка N изображений
    images = models.ForeignKey(
        'Gallery.Gallery',
        verbose_name="Изображения",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    file = models.FileField("Файл", upload_to="callboard_file/", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    moderation = models.BooleanField("Модерация", default=False)
    slug = models.SlugField("url", max_length=200, unique=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("advert_detail", kwargs={"category": self.category.slug, "slug": self.slug})

    # def get_absolute_url(self):
    #     return reverse('advert_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Объявлениe"
        verbose_name_plural = "Объявления"

    # send_notification, который отправляет электронное письмо подписчикам при добавлении новой статьи:
    def send_notification(self):
        subscribers = self.category.subscribers.all()
        for subscriber in subscribers:
            subject = self.name
            html_message = render_to_string('welcome_email.html', {
                'header': f'<h1>{self.name}</h1>',
                'preview': self.preview(),
                'username': subscriber.username,
            })
            plain_message = strip_tags(html_message)
            from_email = 'poc47a.t@yandex.ru'
            to_email = subscriber.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    description = models.ForeignKey(Advert, verbose_name="сообщение", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.description}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


# Создаем свой набор фильтров для модели
# FilterSet, который мы наследуем,
class AdvertFilters(FilterSet):
   category = ModelMultipleChoiceFilter(
      field_name='category',
      queryset=Category.objects.all(),
      # label='Category',
      # empty_label='Выберите вариант'
   )
   created =DateFilter(
       field_name='created',
       lookup_expr='gt',
       widget=forms.DateInput(attrs={'type': 'date'}),
       label='Дата'
   )

   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Advert
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'subject': ['icontains'],
           'created': ['gt'],
           'category': ['exact'],
           'price': [
               'lt',  # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ]
       }



