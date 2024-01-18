from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # base url of the website
    path("todos/", views.todos, name="Todos")
]