from datetime import datetime
from decimal import Decimal

from categories.models import Category
from expenses.models import Expense
from spendalot import constants


class HistoricalParser(object):
    HEADERS = ['Description', 'Category', 'Amount', 'Date', 'Payment']

    def parse(self, row):
        description, category_name, amount, transaction_date, payment = row
        category = Category.objects.get(name=category_name)
        Expense.objects.create(
            description=description,
            payment=payment,
            amount=Decimal(amount),
            date=datetime.strptime(transaction_date, '%m/%d/%Y'),
            category=category,
        )


class LegacyMastercardParser(object):
    HEADERS = ['Transaction Date', 'Posting Date', 'Billing Amount', 'Merchant', 'Merchant City', 'Merchant State', 'Merchant Zip', 'Reference Number', 'Debit/Credit Flag', 'SICMCC Code']

    def parse(self, row):
        transaction_date, posting_date, billing_amount, merchant, merchant_city, merchant_store, merchant_zip, reference_number, debit_credit_flag, sicmcc_code = row
        if debit_credit_flag == 'C':  # Skip payment lines
            return None

        amount = Decimal(billing_amount[1:])
        date = datetime.strptime(transaction_date, '%m/%d/%Y')
        description = merchant.strip().title()
        if Expense.objects.filter(description=description, date=date, amount=amount).count():
            return None

        Expense.objects.create(
            description=description,
            payment=constants.CREDIT_CARD,
            amount=amount,
            date=date,
        )


class MastercardParser(object):
    HEADERS = ['Merchant Name', 'Card Used For Transaction', 'Date', 'Time', 'Amount']

    def parse(self, row):
        merchant_name, card_used, transaction_date, transaction_time, amount = row
        description = merchant_name.strip().title()
        transaction_datetime = '{} {}'.format(transaction_date, transaction_time)
        transaction_datetime = datetime.strptime(transaction_datetime, '%m/%d/%Y %I:%M %p')
        amount = Decimal(amount)
        if amount <= Decimal(0):
            return None

        if Expense.objects.filter(description=description, date=transaction_datetime, amount=amount).count():
            return None

        Expense.objects.create(
            description=description,
            payment=constants.CREDIT_CARD,
            amount=amount,
            date=transaction_datetime
        )


class ParserFactory(object):
    PARSERS = [
        HistoricalParser,
        LegacyMastercardParser,
        MastercardParser
    ]

    def __init__(self, csv_header):
        self.csv_heaer = csv_header

    def create(self):
        for parser in self.PARSERS:
            first_header = self.csv_header[0].replace('\ufeff', '').replace('"', '')
            if first_header == parser.HEADERS[0]:
                return parser
        return None
