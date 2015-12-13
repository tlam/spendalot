from datetime import datetime
import csv

from django.core.cache import cache
from django.db import models
import pandas as pd

from keywords.models import Keyword


PAYMENT_CHOICES = (
    ('CA', 'Cash'),
    ('CC', 'Credit Card'),
)


class Expense(models.Model):
    description = models.CharField(max_length=200)
    payment = models.CharField(max_length=5, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey('categories.Category', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return u'{}'.format(self.description)

    @classmethod
    def cached(self):
        if 'expenses' in cache:
            return cache.get('expenses')
        else:
            expenses = Expense.objects.order_by('-date')
            cache.set('expenses', expenses)
            return expenses

    @classmethod
    def write_csv(self):
        expenses = self.cached()
        with open('data.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Description', 'Category', 'Amount', 'Date', 'Payment'])
            for expense in expenses:
                if not expense.category:
                    continue
                writer.writerow([
                    expense.description.encode('utf-8'),
                    expense.category.name,
                    expense.amount,
                    expense.date.strftime('%Y-%m-%d'),
                    expense.payment,
                ])

    @classmethod
    def data_frame(self):
        if 'data_frame' in cache:
            return cache.get('data_frame')
        else:
            Expense.write_csv()
            df = pd.read_csv('data.csv', parse_dates=['Date'], index_col='Date')
            cache.set('data_frame', df)
            return df

    @classmethod
    def monthly(self, year=datetime.now().year):
        data = {}
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        for expense in self.cached().filter(date__gte=start_date, date__lte=end_date):
            month = expense.date.strftime('%B %Y')
            month = datetime(expense.date.year, expense.date.month, 1)
            if not month in data:
                data[month] = []
            data[month].append(expense)
        data = sorted(data.iteritems())
        data.reverse()
        return data

    @classmethod
    def assign_categories(self):
        keywords = Keyword.objects.all()
        for expense in Expense.objects.filter(category=None):
            for keyword in keywords:
                if keyword.words.lower() in expense.description.lower():
                    expense.category = keyword.category
                    expense.save()

    @classmethod
    def year_range(self):
        expenses = self.cached()
        min_date = expenses.aggregate(models.Min('date'))
        max_date = expenses.aggregate(models.Max('date'))
        return  range(min_date['date__min'].year, max_date['date__max'].year + 1)
