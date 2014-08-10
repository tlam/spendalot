from django.shortcuts import render

from expenses.models import Expense


def index(request):
    monthly = Expense.monthly()

    context = {
        'monthly_expenses': monthly,
    }
    return render(
        request,
        'expenses/index.html',
        context)
