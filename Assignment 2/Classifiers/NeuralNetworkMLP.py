from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
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
            else:
                X.append(row[1])
                y.append(row[0])
            if line_count == 100:
                break
            line_count += 1
print(line_count)

vector = CountVectorizer(stop_words=stop_words)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(8, 5))

pipeLine = Pipeline([('vectorizer', vector), ('classifier', clf)])
pipeLine.fit(X, y)

'''list_pickle_path = 'NeuralNetwork.pkl'
list_pickle = open(list_pickle_path, 'wb')
pickle.dump(pipeLine, list_pickle)
list_pickle.close()'''


X_test = vector.transform(X_test)
y_result = clf.predict(X_test)

print(accuracy_score(y_test,y_result))


endTime = time.time()
print('Loaded Training Data in ' + str(endTime-startTime) + '\n\n')
