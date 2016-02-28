from django.shortcuts import render

from expenses.models import Expense


def home(request):
    total_transactions = Expense.objects.count()
    context = {
        'total_transactions': total_transactions,
    }
    return render(request, 'home.html', context)
