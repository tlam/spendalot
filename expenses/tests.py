from datetime import datetime
from decimal import Decimal

from django.test import Client, RequestFactory, TestCase

from categories.models import Category
from expenses.forms import ExpenseForm
from expenses.models import Expense, DATA_PATH
from expenses.views import create, descriptions
from spendalot import constants


class ExpenseTestCase(TestCase):
    fixtures = ["categories.json", "expenses.json"]

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Test", slug="test")

    def test_create_view(self):
        request = self.factory.get("/expenses/create")
        response = create(request)
        self.assertEqual(response.status_code, 200)

    def test_create_form(self):
        form_data = {}
        form = ExpenseForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "amount": Decimal("10.12"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": "Testing expense",
            "category": self.category.id,
        }
        form = ExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(Expense.objects.count(), 1)
        form.save()
        self.assertEqual(Expense.objects.count(), 2)

    def test_descriptions(self):
        client = Client()
        response = client.get("/expenses/descriptions.json?term=spot")
        self.assertEqual(response.content.decode("utf-8"), '["Spotify"]')

    def test_cached(self):
        self.assertEqual(Expense.cached().count(), 1)

    def test_write_csv(self):
        Expense.write_csv()
        fp = open(DATA_PATH, "r")
        content = fp.read()
        self.assertTrue("Spotify,Entertainment" in content)
        fp.close()

    def test_data_frame(self):
        df = Expense.data_frame()
        self.assertEqual(df.Description[0], "Spotify")

    def test_monthly(self):
        output = Expense.monthly()
        self.assertEqual(
            output, [(datetime(2016, 2, 1, 0, 0), [Expense.objects.get(pk=1)])]
        )

    def test_year_range(self):
        self.assertEqual(Expense.year_range(), range(2016, 2017))

    def test_assign_categories(self):
        for i in range(0, 3):
            expense = Expense.objects.create(
                description="Spotify {}".format(i + 1),
                payment=constants.CREDIT_CARD,
                amount=Decimal("9.99"),
                date=datetime.now(),
            )
            self.assertIsNone(expense.category)

        Expense.assign_categories()

        for expense in Expense.objects.all():
            self.assertEqual(expense.category.name, "Entertainment")
