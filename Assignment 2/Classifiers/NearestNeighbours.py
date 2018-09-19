from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import csv
import time
startTime = time.time()

X = []
y = []
X_test = []
y_test = []
stop_words = set(stopwords.words('english'))
with open('reviews.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if line_count % 5 == 0:
                X_test.append(row[1])
                y_test.append(row[0])
            else:
                X.append(row[1])
                y.append(row[0])
            if line_count == 100000:
                break
            line_count += 1
print(line_count)


vector = CountVectorizer(input='content', encoding='utf-8', decode_error='strict', strip_accents=None, lowercase=True,
                         preprocessor=None, tokenizer=None, analyzer='word', stop_words=stop_words, ngram_range=(1, 1),
                         max_df=1.0, min_df=1, max_features=None,vocabulary=None, binary=False)
X = vector.fit_transform(X)


clf = KNeighborsClassifier(n_neighbors=50)
clf.fit(X, y)


X_test = vector.transform(X_test)
y_result = clf.predict(X_test)
print(accuracy_score(y_test,y_result))


endTime = time.time()
print('Loaded Training Data in ' + str(endTime-startTime) + '\n\n')
