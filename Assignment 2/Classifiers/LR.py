from sklearn import linear_model
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
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
            #if line_count == 10000:
                #break
            line_count += 1

print(line_count)

vector = CountVectorizer(stop_words=stop_words)
clf = linear_model.LogisticRegression(C=1e5)

pipeLine = Pipeline([('vectorizer', vector), ('classifier', clf)])
pipeLine.fit(X, y)

X_test = vector.transform(X_test)
y_result = clf.predict(X_test)
y_probability = clf.predict_proba(X_test)
y_result_01 = []
y_test_01 = []

for x in range(0, len(y_result)):
    if y_result[x] == 'negative':
        y_result_01.append(0)
    else:
        y_result_01.append(1)

    if y_test[x] == 'negative':
        y_test_01.append(0)
    else:
        y_test_01.append(1)

#Accuracy
print("Accuracy:", accuracy_score(y_test, y_result))

#Precision-Recall
print("Precision Score",precision_score(y_test_01, y_result_01))
print("Recall Score",recall_score(y_test_01, y_result_01))

#ROC
roc_ac = roc_auc_score(y_test_01, y_result_01)

fpr, tpr, _ = roc_curve(y_test_01, y_result_01)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='black',
         lw=lw, label='Logistic Regression')
plt.plot([0, 1], [0, 1], color='red', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC')
plt.legend(loc="lower right")
plt.show()

endTime = time.time()
print('Loaded Training Data in ' + str(endTime-startTime) + '\n\n')
