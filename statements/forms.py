from io import StringIO
import csv

from django import forms

from expenses.models import Expense
from statements.parsers import ParserFactory


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def handle_uploaded_file(self, f):
        csv_buffer = StringIO(f.read().decode())
        reader = csv.reader(csv_buffer)
        count = 0
        parsing = ''
        parser = None
        for row in reader:
            count += 1

            if count == 1:
                # TODO: Use CSV Sniffer
                header = row
                for header_type, headers in ParserFactory.HEADERS.items():
                    first_header = header[0].replace('\ufeff', '').replace('"', '')
                    if first_header == headers[0]:
                        parsing = header_type
                        break
                if parsing:
                    continue

            parser = ParserFactory().get(parsing)
            if not parsing or not parser:
                break

            parser.parse(row)
        Expense.assign_categories()
