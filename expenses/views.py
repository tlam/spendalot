from django.shortcuts import render


def index(request):
    context = {}
    return render(
        request,
        'expenses/index.html',
        context)
