# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import pprint

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand
import requests

from expenses.models import Expense


class Command(BaseCommand):

    def handle(self, *args, **options):  # pragma: no cover
        search_url = settings.BLOG_URL  + '/api/search/?categories=places&q={restaurant}'
        expenses = Expense.objects.filter(
            category__name='Restaurant',
            cuisine='').order_by('-date')
        print(expenses.count())
        count = 0
        for expense in expenses:
            print(expense, expense.date)
            response = requests.get(search_url.format(restaurant=expense.description))
            if response.ok:
                output = response.json()
                for result in output['results']:
                    response = requests.get('{}{}'.format(settings.BLOG_URL, result['path']))
                    if response.ok:
                        soup = BeautifulSoup(response.content, 'lxml')
                        for tag in soup.find_all('script'):
                            if tag.attrs.get('type') == 'application/ld+json':
                                name_so_far = ''
                                for item in json.loads(tag.string).get('itemListElement', []):
                                    if item['position'] == 3:
                                        if item['item']['name'] != 'None':
                                            name_so_far = item['item']['name']
                                        print(name_so_far)
                                        expense.cuisine = name_so_far
                                        expense.save()
                                        break
                                    else:
                                        name_so_far = item['item']['name']

                    break
                count += 1

            #if count == 10:
            #    break
