import csv
import os

try:
    from sklearn import preprocessing
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    from sklearn.linear_model import SGDClassifier
    from sklearn.pipeline import Pipeline
    import pandas as pd
except ImportError:
    pass


class Learn(object):

    def __init__(self, refresh=False):
        file_name = 'expenses.csv'
        if not os.path.isfile(file_name) or refresh:
            from expenses.models import Expense
            with open(file_name, 'wb') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'Category'])
                for expense in Expense.objects.all():
                    writer.writerow([expense.description.encode('utf-8'), expense.category.name])

        df = pd.read_csv(file_name)
        data = df.Name.tolist()
        categories = df.Category.tolist()
        self.unique_categories = df.Category.unique().tolist()
        self.unique_categories.sort()
        le = preprocessing.LabelEncoder()
        le.fit(categories)
        target = le.transform(categories)

        self.text_clf = Pipeline([
            ('vect', CountVectorizer()),  # Bag of words
            ('tfidf', TfidfTransformer()),  # term frequency-inverse document frequency
            ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),  # SVM classifier
        ])

        self.text_clf = self.text_clf.fit(data, target)

    def predict(self, description):
        search_terms = [description]
        predicted = self.text_clf.predict(search_terms)

        for search, category in zip(search_terms, predicted):
            return self.unique_categories[category]

        return ''
