from django.http import HttpResponse
from django.shortcuts import render

from categories.models import Category
from expenses.models import Expense


def index(request):
    context = {
        'categories': Category.objects.all(),
    }
    return render(request, 'categories/index.html', context)


def details(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'category': category,
    }
    return render(request, 'categories/details.html', context)


def details_json(request, slug):
    df = Expense.data_frame()
    categories = df.groupby('Category')
    category = Category.objects.get(slug=slug).name
    yearly = categories.get_group(category).resample('A', how='sum')
    monthly = categories.get_group(category).resample('M', how='sum')
    monthly_mean = monthly.mean()['Amount']
    yearly_mean = yearly.mean()['Amount']
    yearly.index = yearly.index.map(lambda t: t.strftime('%Y'))
    monthly.index = monthly.index.map(lambda t: t.strftime('%b %Y'))

    return HttpResponse(monthly.to_json(), mimetype='application/javascript')
