from django.urls import path

from .views import AdvertList, AdvertDetail, AdvertCreate, AdvertUpdate, AdvertDelete
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='callboard/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='callboard/logout.html'),
         name='logout'),
    path('callboardup/',
         BaseRegisterView.as_view(template_name='callboard/callboardup.html'),
         name='callboardup'),

    path("", AdvertList.as_view(), name="advert_list"),

    path('create/', AdvertCreate.as_view(), name='advert_create'),
    path('<slug:category>/<slug:slug>/update/', AdvertUpdate.as_view(), name='advert_update'),
    path('<slug:category>/<slug:slug>/delete/', AdvertDelete.as_view(), name='advert_delete'),
    path("<slug:category>/<slug:slug>/", AdvertDetail.as_view(), name="advert_detail"),
    path('upgrade/', upgrade_me, name = 'upgrade')
    # path("profiles/", ProfileView.as_view(), name="user_detail"),
    # path("update/<int:pk>/", ProfileUpdateView.as_view(), name='user_update'),
    #path('success/', AdvertFiltrForm.as_view(), name="advert_filter"),
]