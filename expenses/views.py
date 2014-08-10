from django.shortcuts import render

from expenses.models import Expense


def index(request):
    expenses = Expense.cached()

    context = {
        'expenses': expenses,
    }
    return render(
        request,
        'expenses/index.html',
        context)
