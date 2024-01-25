from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # base url of the website
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("todos/", views.todos, name="Todos")
]