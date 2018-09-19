#87.8
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
import csv
import time
import pickle

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
            #else:
            X.append(row[1])
            y.append(row[0])
            line_count += 1

print(line_count)
vector = CountVectorizer(stop_words=stop_words, lowercase=True)
clf = linear_model.LogisticRegression(C=1e5)

pipeLine = Pipeline([('vectorizer', vector), ('classifier', clf)])
pipeLine.fit(X, y)

'''list_pickle_path = 'LogisticRegression.pkl'
list_pickle = open(list_pickle_path, 'wb')
pickle.dump(pipeLine, list_pickle)
list_pickle.close()'''

X_test = vector.transform(X_test)
y_result = clf.predict(X_test)
print(accuracy_score(y_test, y_result))


endTime = time.time()
print('Loaded Training Data in ' + str(endTime-startTime) + '\n\n')
