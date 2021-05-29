from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.pd = []
        self.dictionary = dict()

    def fit(self, x1, y, y_d):
        self.pd = [0] * len(y_d)
        for i in range(len(y)):
            w = x1[i].split()
            self.pd[y_d[y[i]]] += 1
            for j in w:
                if j not in self.dictionary:
                    self.dictionary[j] = [0] * (2 * len(y_d) + 1)
                self.dictionary[j][y_d[y[i]]] += 1
                self.dictionary[j][2 * len(y_d)] += 1
        nt = [0] * len(y_d)
        for i in self.dictionary.keys():
            for j in range(len(y_d)):
                nt[j] += self.dictionary[i][j]
        for i in self.dictionary.keys():
            for j in range(len(y_d)):
                self.dictionary[i][len(y_d) + j] = (self.dictionary[i][j] + self.alpha) / (
                        self.dictionary[i][2 * len(y_d)] + self.alpha * len(self.dictionary))

    def predict(self, x1):
        arr = []
        for i in range(len(x1)):
            w = x1[i].split()
            pb = [log(i) for i in self.pd]
            for j in w:
                for k in range(len(self.pd)):
                    if j not in self.dictionary:
                        continue
                    pb[k] += log(self.dictionary[j][len(self.pd) + k])
            min1 = 0
            max1 = pb[0]
            for j in range(1, len(self.pd)):
                if pb[j] > max1:
                    max1 = pb[j]
                    min1 = j
                    print(x1[i], pb)
            arr.append(min1)
        return arr

    def score(self, x1_test, y_test, y_d):
        count = 0
        arr = [y_d[i] for i in y_test]
        pd = self.predict(x1_test)
        for i in range(len(y_test)):
            if pd[i] == arr[i]:
                count += 1
        return count / len(y_test)

x = [
    "i love this sandwich",
    "this is an amazing place",
    "i feel very good about these beers",
    "this is my best work",
    "what an awesome view",
    "i do not like this restaurant",
    "i am tired of this stuff",
    "i cant deal with this",
    "he is my sworn enemy",
    "my boss is horrible",
]
y = [
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
]
x_test = [
    "the beer was good",
    "i do not enjoy my job",
    "i aint feeling dandy today",
    "i feel amazing",
    "gary is a friend of mine",
    "i cant believe im doing this",
]
y_test = ["Positive", "Negative", "Negative", "Positive", "Positive", "Negative"]
y_dict = {"Positive": 0, "Negative": 1}
test = NaiveBayesClassifier(0.1)
test.fit(x, y, y_dict)

print(test.score(x_test, y_test, y_dict))