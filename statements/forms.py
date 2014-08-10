from datetime import datetime
from decimal import Decimal
import csv

from django import forms

from categories.models import Category
from expenses.models import Expense


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def handle_uploaded_file(self, f):
        reader = csv.reader(f)
        count = 0
        for row in reader:
            count += 1
            if count == 1:
                header = row
                if header == ['Description', 'Category', 'Amount', 'Date', 'Payment']:
                    print 'Parsing historical data'
                continue
            description, category_name, amount, transaction_date, payment = row
            category = Category.objects.get(name=category_name)
            Expense.objects.create(
                description=description,
                payment=payment,
                amount=Decimal(amount),
                date=datetime.strptime(transaction_date, '%m/%d/%Y'),
                category=category,
            )
