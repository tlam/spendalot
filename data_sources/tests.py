from django.test import TestCase

from data_sources.learn import Learn


class DataSourcesTestCase(TestCase):
    fixtures = ['categories.json', 'sample.json']

    def test_learn(self):
        learn = Learn(refresh=True)
        prediction = learn.predict('spotify')
        self.assertEqual(prediction, 'Entertainment')

        prediction = learn.predict('metro')
        self.assertEqual(prediction, 'Grocery')
