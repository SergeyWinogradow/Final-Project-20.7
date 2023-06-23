from django.urls import path
from . import views
from .views import IndexView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('', IndexView.as_view()),
    path("<int:pk>", ProfileView.as_view(), name="user_detail"),
    path("update/<int:pk>/", ProfileUpdateView.as_view(), name='user_update'),
    # path("adverts/", views.UserAdvertList.as_view()),
    # path("update-adverts/<int:pk>/", views.UserAdvertUpdate.as_view()),
]
