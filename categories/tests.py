from django.test import RequestFactory, TestCase

from categories.models import Category
from categories.views import details, index


class CategoryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        Category.objects.create(name="Grocery", slug="grocery")
        Category.objects.create(name="Restaurant", slug="restaurant")

    def test_create(self):
        name = "Test"
        slug = name.lower()
        category = Category.objects.create(name=name, slug=slug)
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, slug)

    def test_index(self):
        request = self.factory.get("/categories/")
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_details(self):
        request = self.factory.get("/categories/grocery/")
        response = details(request, "grocery")
        self.assertEqual(response.status_code, 200)
