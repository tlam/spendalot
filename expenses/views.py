from datetime import datetime
from decimal import Decimal
import json

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

from expenses.forms import ExpenseForm, TrendsForm
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
            expense = form.save()
            expense.payment = 'CA'
            expense.save()
            messages.success(request, 'Expense created')
            return redirect('expenses:create')
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
        expenses = Expense.cached().filter(description__icontains=keyword).order_by('description').distinct('description')
        data = [expense.description for expense in expenses]
    else:
        data = []

    return HttpResponse(json.dumps(data), mimetype='application/javascript')


def category(request):
    description = request.GET.get('description', '')
    data = {
        'category_id': 0,
    }
    if description:
        expenses = Expense.cached().filter(description=description)
        if expenses:
            data['category_id'] = expenses[0].category.id

    return HttpResponse(json.dumps(data), mimetype='application/javascript')


def trends(request):
    context = {'expenses': []}
    if request.method == 'POST':
        form = TrendsForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            expenses = Expense.cached().filter(description__icontains=description).order_by('-date')
            context['sum'] = expenses.aggregate(expenses_sum=Sum('amount')).get('expenses_sum', Decimal(0))
            context['expenses'] = expenses
    else:
        form = TrendsForm()

    context['form'] = form

    return render(
        request,
        'expenses/trends.html',
        context,
    )
