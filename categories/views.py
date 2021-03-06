import collections

from django.http import JsonResponse
from django.shortcuts import render

from categories.models import Category
from categories.forms import PredictionForm
from data_sources.learn import Learn
from expenses.models import Expense


def index(request):
    context = {
        'categories': Category.objects.all(),
    }
    return render(request, 'categories/index.html', context)


def categories_json(request):
    categories = Category.objects.all()
    json_data = {
        'categories': []
    }
    for category in categories:
        json_data['categories'].append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'url': category.get_absolute_url()
        })
    return JsonResponse(json_data)


def details(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'categories': Category.objects.all(),
        'category': category,
    }
    return render(request, 'categories/details.html', context)


def details_json(request, slug):
    df = Expense.data_frame()
    categories = df.groupby('Category')
    category = Category.objects.get(slug=slug).name
    yearly = categories.get_group(category).resample('A').sum()
    yearly = yearly.fillna(0)
    monthly = categories.get_group(category).resample('M').sum()
    monthly = monthly.fillna(0)

    monthly_mean = monthly.mean()['Amount']
    yearly_mean = yearly.mean()['Amount']
    yearly.index = yearly.index.map(lambda t: t.strftime('%Y'))
    monthly.index = monthly.index.map(lambda t: t.strftime('%b %Y'))

    category_data = {
        'name': category,
        'monthly_mean': '{0:.2f}'.format(monthly_mean),
        'sum': '{0:.2f}'.format(categories.get_group(category).sum()['Amount']),
        'yearly_mean': '{0:.2f}'.format(yearly_mean),
    }

    json_data = {
        'category': category_data,
        'monthly': monthly.to_dict(into=collections.OrderedDict),
        'yearly': yearly.to_dict()
    }
    return JsonResponse(json_data)


def category_stats_json(request):
    df = Expense.data_frame()
    categories = df.groupby('Category')
    data = {}
    for category in Category.objects.all():
        if category.name in categories.groups:
            data[category.name] = '{:.2f}'.format(categories.get_group(category.name).sum()['Amount'])

    return JsonResponse(data)


def prediction(request):
    category = ''
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            learn = Learn()
            category = learn.predict(keywords)
    else:
        form = PredictionForm()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'categories/prediction.html', context)
