from datetime import datetime, timedelta
from decimal import Decimal
import collections
import csv
import json

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

from expenses.forms import ExpenseForm, TrendsForm
from expenses.models import Expense
from spendalot import constants


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
            expense.payment = constants.CASH
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

    return HttpResponse(json.dumps(data), content_type='application/javascript')


def category(request):
    description = request.GET.get('description', '')
    data = {
        'category_id': 0,
    }
    if description:
        expenses = Expense.cached().filter(description=description)
        if expenses:
            data['category_id'] = expenses[0].category.id

    return HttpResponse(json.dumps(data), content_type='application/javascript')


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


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    for expense in Expense.objects.all():
        writer.writerow([expense.description.encode('utf-8'), expense.category.name])

    return response


def cuisines(request):
    days = 30
    past = datetime.now() - timedelta(days=days)
    expenses = Expense.objects.filter(
        category__name='Restaurant',
        date__gte=past).order_by('-date')

    last_year = Expense.objects.filter(
        category__name='Restaurant',
        date__gte=past - timedelta(days=365),
        date__lte=datetime.now() - timedelta(days=365)).order_by('-date')

    df = Expense.data_frame()
    top_cuisines = df.groupby(['Cuisine']).count().sort_values('Category', ascending=False).head(40)
    context = {
        'days': days,
        'expenses': expenses,
        'last_year': last_year,
        'top_cuisines': top_cuisines['Category'].to_dict(into=collections.OrderedDict)
    }
    return render(
        request,
        'expenses/cuisines.html',
        context)
