import os

from django.conf import settings
from django.test import TestCase

from expenses.models import Expense
from statements.forms import UploadFileForm


class StatementTestCase(TestCase):

    def test_uploaded_file(self):
        self.assertEqual(Expense.objects.count(), 0)
        fp = open(
            os.path.join(settings.BASE_DIR, "statements", "fixtures", "statement.csv"),
            "r",
        )
        form = UploadFileForm()
        form.handle_uploaded_file(fp)
        fp.close()
        self.assertEqual(Expense.objects.count(), 7)
