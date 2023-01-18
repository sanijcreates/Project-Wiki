from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name = "newpage"),
    path("editpage", views.editpage, name = "editpage"),
    path("wiki/<str:title>", views.entry, name = "entry"),
    path("/search", views.search, name = "search"),
    path("save_page/", views.save_page, name = "save_page"),
    path("random_page/", views.random_page, name = "random_page")
]
