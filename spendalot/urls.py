from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from . import views


admin.autodiscover()

urlpatterns = [
    path(r"", views.home, name="home"),
    path(
        r"categories/",
        include("categories.urls", namespace="categories"),
        name="categories",
    ),
    path(r"expenses/", include("expenses.urls", namespace="expenses"), name="expenses"),
    path(
        r"statements/",
        include("statements.urls", namespace="statements"),
        name="statements",
    ),
    path(r"admin/", admin.site.urls),
]
