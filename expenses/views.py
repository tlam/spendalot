from datetime import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

from expenses.forms import ExpenseForm
from expenses.models import Expense


def index(request):
    year = int(request.GET.get('year', datetime.now().year))
    monthly = Expense.monthly(year)

    context = {
        'year_range': Expense.year_range(),
        'monthly_expenses': monthly,
    }
    return render(
        request,
        'expenses/index.html',
        context)


def create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ExpenseForm()
    context = {
        'form': form,
    }

    return render(
        request,
        'expenses/create.html',
        context)


def descriptions(request):
    keyword = request.GET.get('term', '')
    if keyword:
        expenses = Expense.cached().filter(description__icontains=keyword)
        data = [expense.description for expense in expenses]
    else:
        data = []

    return HttpResponse(json.dumps(data), mimetype='application/javascript')
