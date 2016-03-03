import json

from django.http import HttpResponse
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
    yearly = categories.get_group(category).resample('A', how='sum')
    yearly = yearly.fillna(0)
    monthly = categories.get_group(category).resample('M', how='sum')
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

    # Concatenate the json data because because panda outputs sorted json
    json_data = '''
        {{
            "category": {},
            "monthly": {},
            "yearly": {}
        }}
    '''.format(json.dumps(category_data), monthly.to_json(), yearly.to_json())

    return HttpResponse(json_data, content_type='application/javascript')


def categories_json(request):
    df = Expense.data_frame()
    total = df.sum()['Amount']
    categories = df.groupby('Category')
    data = {}
    for category in Category.objects.all():
        data[category.name] = '{:.2f}'.format((categories.get_group(category.name).sum()['Amount'] * 100) / total)

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/javascript')


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
