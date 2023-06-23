from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import datetime
from .models import Advert, Category
from .forms import AdvertForm

from django.contrib.auth.models import User

from .models import BaseRegisterForm


from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404, reverse

class CategoryListView(ListView):
    model = Advert
    template_name = 'advert_detail.html'
    context_object_name = 'advert_detail'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Advert.objects.filter(category=self.category).order_by('-created')
        return queryset
    # кнопка для подписки
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required # для тех кто подписан
def subscribe(request, pk):

    user = request.user
    category = get_object_or_404(Category, id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

class AdvertList(ListView):
    # Все объявления
    model = Advert
    ordering = 'created'
    queryset = Advert.objects.all()
    template_name = "callboard/advert_list.html"
    paginate_by = 5  # вот так мы можем указать количество записей на странице

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = "новые молоты поступят в продажу!"
        return context

class AdvertDetail(DetailView):
    # Подробно об объявлении
    model = Advert
    context_object_name = "advert"
    template_name = "callboard/advert_detail.html"

# Добавляем новое представление для создания объявлений.
class AdvertCreate(CreateView):
    """Добавление объявлений"""
    # Указываем нашу разработанную форму
    form_class = AdvertForm
    # модель товаров
    model = Advert
    # и новый шаблон, в котором используется форма.
    template_name = 'callboard/advert_edit.html'

class AdvertUpdate(UpdateView):
    """Добавление объявлений"""
    # Указываем нашу разработанную форму
    form_class = AdvertForm
    # модель товаров
    model = Advert
    # и новый шаблон, в котором используется форма.
    template_name = 'callboard/advert_edit.html'

class AdvertDelete(DeleteView):
    """Добавление объявлений"""
    # Указываем нашу разработанную форму
    form_class = AdvertForm
    # модель товаров
    model = Advert
    # и новый шаблон, в котором используется форма.
    template_name = 'callboard/advert_delete.html'




# class AdvertFiltrForm(FormView):
#     form_class = AdvertFiltrForm
#     model = Advert
#     template_name = 'callboard/advert_filtr.html'
#     #success_url = 'advert/success/'
#
#     def get_queryset(self):
#         queryset = Advert.objects.all()
#         self.filterset = AdvertFilters(self.request.GET, queryset)
#         return self.filterset.qs
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#     # Метод get_context_data позволяет нам изменить набор данных,
#     # который будет передан в шаблон.
#     def get_context_data(self, **kwargs):
#         # С помощью super() мы обращаемся к родительским классам
#         # и вызываем у них метод get_context_data с теми же аргументами,
#         # что и были переданы нам.
#         # В ответе мы должны получить словарь.
#         context = super().get_context_data(**kwargs)
#         # К словарю добавим текущую дату в ключ 'time_now'.
#         context['time_now'] = datetime.utcnow()
#         # Добавим ещё одну пустую переменную,
#         # чтобы на её примере рассмотреть работу ещё одного фильтра.
#         context['next_sale'] = "поиск по отрибутам"
#         return context
#
#
# class AdvertList(generics.ListAPIView):
#     """Все объявления"""
#     permission_classes = [permissions.AllowAny]
#     queryset = Advert.objects.all()
#     serializer_class = AdvertListSer
#
# class AdvertDetail(generics.RetrieveAPIView):
#     # Подробно об объявлении
#     permission_classes = [permissions.AllowAny]
#     queryset = Advert.objects.all()
#     lookup_field = 'slug'
#     serializer_class = AdvertDetailSer
#
# class AdvertCreate(generics.CreateAPIView):
#     """Добавление объявлений"""
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Advert.objects.all()
#     serializer_class = AdvertCreateSer