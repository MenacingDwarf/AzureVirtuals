from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name="hello"),
    path('add_task/', views.add_task, name="add_task")
]
