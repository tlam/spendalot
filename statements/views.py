from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'statements/index.html', context)
