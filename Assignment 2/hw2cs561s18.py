import sys
import pickle

#inputFile = open(sys.argv[2], "r")
inputFile = open("input1.txt", "r")
outputFile = open("output.txt", "w")

X = [inputFile.readline()]

list_pickle_path = 'NeuralNetwork.pkl'
list_unpickle = open(list_pickle_path, 'r')
clf = pickle.load(list_unpickle)
pre = clf.predict(X)[0]
if pre == 'negative':
    outputFile.write('0')
elif pre == 'positive':
    outputFile.write('1')
