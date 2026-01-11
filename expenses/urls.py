from django.urls import re_path

from . import views


app_name = "expenses"
urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^category.json$", views.category, name="category"),
    re_path(r"^cuisines/$", views.cuisines, name="cuisines"),
    re_path(r"^download-csv/$", views.download_csv, name="download-csv"),
    re_path(r"^create/$", views.create, name="create"),
    re_path(r"^descriptions.json$", views.descriptions, name="descriptions"),
    re_path(r"^trends/$", views.trends, name="trends"),
]
