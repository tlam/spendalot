from datetime import datetime
from decimal import Decimal
import csv
import os

from django.conf import settings
import dropbox

from expenses.models import Expense
from spendalot import constants


class DropboxClient(object):

    def __init__(self):
        self.client = dropbox.Dropbox(settings.DROPBOX_API['access_token'])
        self.data_path = os.path.join(settings.BASE_DIR, 'spendalot', 'static', 'data_sources', 'dropbox')
        self.output_path = '/tmp/output.csv'

    def download_file(self):
        latest_file = ''
        latest_date = None
        for entry in self.client.files_list_folder('/ExpenseManager/CSV').entries:
            print entry.name, entry.client_modified
            if latest_date:
                if entry.client_modified > latest_date:
                    latest_date = entry.client_modified
                    latest_file = entry.path_display
            else:
                latest_date = entry.client_modified
                latest_file = entry.path_display
        self.client.files_download_to_file(self.output_path, latest_file)

    def load_expenses(self):
        self.download_file()
        with open(self.output_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 7:
                    continue
                try:
                    transaction_date = datetime.strptime(row[0], '%Y-%m-%d')
                except ValueError:
                    continue
                amount = Decimal(row[1]) * Decimal(-1)
                description = row[7].title()
                if Expense.objects.filter(description=description, date=transaction_date, amount=amount).count():
                    continue

                Expense.objects.create(
                    description=description,
                    payment=constants.CASH,
                    amount=amount,
                    date=transaction_date,
                )
        Expense.assign_categories()
