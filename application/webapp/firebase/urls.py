from django.urls import path
from . import views
from .views import CreateUser,UpdateUser,DeleteUser

urlpatterns = [
    path('', views.index, name="index"),
    path('list', views.list, name="list"),
    path('details/<uid>/', views.details, name="details"),
    path('token', views.token, name="token"),
    path('createuser', CreateUser.as_view(), name='createuser'),
    path('updateuser', UpdateUser.as_view(), name='updateuser'),
    path('deleteuser', DeleteUser.as_view(), name='deleteuser'),
]
