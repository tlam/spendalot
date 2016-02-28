from datetime import datetime
from decimal import Decimal
import csv

from django import forms

from categories.models import Category
from expenses.models import Expense
from spendalot import constants

HEADERS = {
    'historical': ['Description', 'Category', 'Amount', 'Date', 'Payment'],
    'mastercard': ['Transaction Date', 'Posting Date', 'Billing Amount', 'Merchant', 'Merchant City', 'Merchant State', 'Merchant Zip', 'Reference Number', 'Debit/Credit Flag', 'SICMCC Code'],
}


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def handle_uploaded_file(self, f):
        reader = csv.reader(f)
        count = 0
        parsing = ''
        for row in reader:
            count += 1
            if count == 1:
                header = row
                if header[0] == HEADERS['historical'][0]:
                    parsing = 'historical'
                elif header[0] == HEADERS['mastercard'][0]:
                    parsing = 'mastercard'
                continue

            if not parsing:
                break

            if parsing == 'historical':
                description, category_name, amount, transaction_date, payment = row
                category = Category.objects.get(name=category_name)
                Expense.objects.create(
                    description=description,
                    payment=payment,
                    amount=Decimal(amount),
                    date=datetime.strptime(transaction_date, '%m/%d/%Y'),
                    category=category,
                )
            else:
                transaction_date, posting_date, billing_amount, merchant, merchant_city, merchant_store, merchant_zip, reference_number, debit_credit_flag, sicmcc_code = row
                if debit_credit_flag == 'C':  # Skip payment lines
                    continue

                amount = Decimal(billing_amount[1:])
                date = datetime.strptime(transaction_date, '%m/%d/%Y')
                description = merchant.strip().title()
                if Expense.objects.filter(description=description, date=date, amount=amount).count():
                    continue

                Expense.objects.create(
                    description=description,
                    payment=constants.CREDIT_CARD,
                    amount=amount,
                    date=date,
                )
        Expense.assign_categories()
