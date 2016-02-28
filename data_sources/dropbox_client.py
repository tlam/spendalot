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
        self.client = dropbox.client.DropboxClient(settings.DROPBOX_API['access_token'])
        self.data_path = os.path.join(settings.BASE_DIR, 'spendalot', 'static', 'data_sources', 'dropbox')

    def download_file(self):
        folder_metadata = self.client.metadata('ExpenseManager/CSV')
        date_format = '%a, %d %b %Y %H:%M:%S +0000'
        latest_file = ''
        latest_date = None
        for content in folder_metadata['contents']:
            date_modified = datetime.strptime(content['modified'], date_format)
            if latest_date:
                if date_modified > latest_date:
                    latest_date = date_modified
                    latest_file = content['path']
            else:
                latest_date = date_modified
                latest_file = content['path']

        f, metadata = self.client.get_file_and_metadata(latest_file)

        file_path = os.path.join(self.data_path, 'output.csv')
        output = open(file_path, 'wb')
        output.write(f.read())
        output.close()
        return file_path

    def load_expenses(self):
        csv_file = self.download_file()
        with open(csv_file, 'rb') as csvfile:
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
