from sklearn import metrics, preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd


df = pd.read_csv('expenses.csv')
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(df.Name.tolist())

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

categories = df.Category.tolist()

le = preprocessing.LabelEncoder()
le.fit(categories)
target = le.transform(categories)
unique_categories = df.Category.unique().tolist()
unique_categories.sort()
print(unique_categories)

# searchsorted to have continuous labels
clf = MultinomialNB().fit(X_train_tfidf, target)

search_terms = ['tim hortons', 'ihop', 'loblaws', 'shoppers', 'Enterprise', 'deer', 'europe bound']
search_terms = ['loblaws']
X_new_counts = count_vect.transform(search_terms)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
for search, category in zip(search_terms, predicted):
    print(search, category, unique_categories[category])
print('DONE')

data = df.Name.tolist()
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])
text_clf = text_clf.fit(data, target)
predicted = text_clf.predict(search_terms)
for search, category in zip(search_terms, predicted):
    print(search, category, unique_categories[category])
print(np.mean(predicted == target))

text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),
])

text_clf = text_clf.fit(data, target)
predicted = text_clf.predict(search_terms)
for search, category in zip(search_terms, predicted):
    print(search, category, unique_categories[category])
