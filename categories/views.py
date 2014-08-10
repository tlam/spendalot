from django.shortcuts import render

from categories.models import Category


def index(request):
    context = {
        'categories': Category.objects.all(),
    }
    return render(request, 'categories/index.html', context)
