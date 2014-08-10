from datetime import datetime
import csv

from django.core.cache import cache
from django.db import models
import pandas as pd

PAYMENT_CHOICES = (
    ('CA', 'Cash'),
    ('CC', 'Credit Card'),
)


class Expense(models.Model):
    description = models.CharField(max_length=200)
    payment = models.CharField(max_length=5, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey('categories.Category')
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now())

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
