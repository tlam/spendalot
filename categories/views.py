import json

from django.http import HttpResponse
from django.shortcuts import render

from categories.models import Category


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
    data = {"Jul 2009":{"sum":"124.91","date":"2009-07-01"},"Mar 2010":{"sum":"5.27","date":"2010-03-01"},"May 2010":{"sum":"68.43","date":"2010-05-01"},"Jul 2010":{"sum":"67.79","date":"2010-07-01"},"Nov 2010":{"sum":"101.68","date":"2010-11-01"},"Dec 2010":{"sum":"25.96","date":"2010-12-01"},"Apr 2011":{"sum":"73.44","date":"2011-04-01"},"Aug 2011":{"sum":"45.19","date":"2011-08-01"},"Dec 2011":{"sum":"45.19","date":"2011-12-01"},"Mar 2012":{"sum":"75.07","date":"2012-03-01"},"Apr 2012":{"sum":"64.84","date":"2012-04-01"},"May 2012":{"sum":"68.0","date":"2012-05-01"},"Jul 2012":{"sum":"33.96","date":"2012-07-01"},"Aug 2012":{"sum":"7.63","date":"2012-08-01"},"Sep 2012":{"sum":"20.11","date":"2012-09-01"},"Nov 2012":{"sum":"71.85","date":"2012-11-01"},"Dec 2012":{"sum":"18.02","date":"2012-12-01"},"Feb 2013":{"sum":"25.0","date":"2013-02-01"},"Mar 2013":{"sum":"79.35","date":"2013-03-01"},"Apr 2013":{"sum":"68.81","date":"2013-04-01"},"May 2013":{"sum":"1.04","date":"2013-05-01"},"Jul 2013":{"sum":"12.81","date":"2013-07-01"},"Sep 2013":{"sum":"5.24","date":"2013-09-01"},"Dec 2013":{"sum":"83.38","date":"2013-12-01"},"Jan 2014":{"sum":"28.67","date":"2014-01-01"},"Feb 2014":{"sum":"22.57","date":"2014-02-01"},"Mar 2014":{"sum":"84.7","date":"2014-03-01"},"May 2014":{"sum":"5.71","date":"2014-05-01"}}
    return HttpResponse(json.dumps(data), mimetype='application/javascript')
