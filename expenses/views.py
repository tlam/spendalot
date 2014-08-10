from django.core.cache import cache
from django.shortcuts import render

from expenses.models import Expense


def index(request):
    if 'expenses' in cache:
        expenses = cache.get('expenses')
    else:
        expenses = Expense.objects.order_by('-date')
        cache.set('expenses', expenses)

    context = {
        'expenses': expenses,
    }
    return render(
        request,
        'expenses/index.html',
        context)
