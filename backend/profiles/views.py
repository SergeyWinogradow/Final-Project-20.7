from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
import os
import sys

# from rest_framework import generics
# from rest_framework import permissions
#
# from backend.callboard.models import Advert
# from backend.callboard.serializers import AdvertListSer, AdvertCreateSer
from .forms import UserForm
from .models import Profile
# from .serializers import ProfileSer, ProfileUpdateSer

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context

class ProfileView(DetailView):
    # профиль пользователя
    form_class = UserForm
    model = Profile
    context_object_name = "profile"
    queryset = Profile.objects.all()
    template_name = "profiles/user_detail.html"

    # def get_queryset(self):
    #     return Profile.objects.get(user__username=self.kwargs.get("slug"))

class ProfileUpdateView(UpdateView):
    # Изменения профиля
    form_class = UserForm
    model = Profile
    context_object_name = "profile"
    queryset = Profile.objects.all()
    template_name = "profiles/user_detail.html"

# class ProfileDetail(generics.RetrieveAPIView):
#     # профиль пользователя
#     # IsAuthenticated - если пользователь авторизован
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSer
#
# class ProfileUpdateView(generics.UpdateAPIView):
#     # редактирование профиля пользователя
#     # IsAuthenticated - если пользователь авторизован
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileUpdateSer
#
# class UserAdvertList(generics.ListAPIView):
#     """Все объявления пользователя"""
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = AdvertListSer
#
#     def get_queryset(self):
#         return Advert.objects.filter(user=self.request.user)
#
# class UserAdvertUpdate(generics.UpdateAPIView):
#     # редактирование объявления пользователя
#     # IsAuthenticated - если пользователь авторизован
#     permission_classes = [permissions.IsAuthenticated]
#
#     serializer_class = AdvertCreateSer
#
#     # только сообщения нашего пользователя
#     def get_queryset(self):
#         return Advert.objects.filter(user=self.request.user)


