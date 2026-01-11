from datetime import datetime
import csv
import os

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils import timezone
import pandas as pd

from categories.models import Category
from data_sources.learn import Learn
from spendalot import constants

DATA_PATH = os.path.join(settings.BASE_DIR, "data_sources", "data.csv")
PAYMENT_CHOICES = (
    (constants.CASH, "Cash"),
    (constants.CREDIT_CARD, "Credit Card"),
)


class Expense(models.Model):
    description = models.CharField(max_length=200)
    payment = models.CharField(max_length=5, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(
        "categories.Category", null=True, blank=True, on_delete=models.CASCADE
    )
    cuisine = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return "{}".format(self.description)

    @property
    def recently_added(self):
        return (timezone.now() - self.created_at).total_seconds() <= 60 * 60

    @classmethod
    def cached(self):
        if "expenses" in cache:
            return cache.get("expenses")
        else:
            expenses = Expense.objects.order_by("-date")
            if expenses:
                cache.set("expenses", expenses)
            return expenses

    @classmethod
    def write_csv(self):
        expenses = self.cached()
        with open(DATA_PATH, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Description", "Category", "Cuisine", "Amount", "Date", "Payment"]
            )
            for expense in expenses:
                if not expense.category:
                    continue
                writer.writerow(
                    [
                        expense.description.encode("utf-8"),
                        expense.category.name,
                        expense.cuisine,
                        expense.amount,
                        expense.date.strftime("%Y-%m-%d"),
                        expense.payment,
                    ]
                )

    @classmethod
    def data_frame(self):
        if "data_frame" in cache:
            return cache.get("data_frame")
        else:
            Expense.write_csv()
            df = pd.read_csv(DATA_PATH, parse_dates=["Date"], index_col="Date")
            cache.set("data_frame", df)
            return df

    @classmethod
    def monthly(self, year=datetime.now().year):
        data = {}
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        for expense in self.cached().filter(date__gte=start_date, date__lte=end_date):
            month = datetime(expense.date.year, expense.date.month, 1)
            if month not in data:
                data[month] = []
            data[month].append(expense)
        data = sorted(data.items(), reverse=True)
        return data

    @classmethod
    def assign_categories(self):
        categories = {}
        for category in Category.objects.all():
            categories[category.name] = category

        learn = Learn()
        for expense in Expense.objects.filter(category=None):
            prediction = learn.predict(expense.description.lower())
            if prediction in categories:
                expense.category = categories[prediction]
                expense.save()

    @classmethod
    def year_range(self):
        expenses = self.cached()
        min_date = expenses.aggregate(models.Min("date"))
        max_date = expenses.aggregate(models.Max("date"))
        return range(min_date["date__min"].year, max_date["date__max"].year + 1)
