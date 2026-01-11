from django.urls import re_path

from . import views


app_name = "categories"
urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^categories.json$", views.categories_json, name="categories_json"),
    re_path(
        r"^category_stats.json$", views.category_stats_json, name="category_stats_json"
    ),
    re_path(r"^prediction/$", views.prediction, name="prediction"),
    re_path(r"^(?P<slug>\w+)/$", views.details, name="details"),
    re_path(r"^(?P<slug>\w+).json$", views.details_json, name="details_json"),
]
