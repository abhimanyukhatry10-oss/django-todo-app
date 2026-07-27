
from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_task, name='add_task'), #name='add_task' → Baad me templates me URL ko name se use kar sakte hain.
    path('update/<int:id>/', views.update_task, name='update_task'),
    path("delete/<int:id>/", views.delete_task, name="delete_task"),
    path("register/", views.register, name="register"),
    path("login/",views.login_user,name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("create-superuser/", views.create_superuser, name="create_superuser"),
]