from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


# Apply KNN classifier
def knn(K,X_train, X_test, y_train):
    classifier = KNeighborsClassifier(n_neighbors = K)
    classifier.fit(X_train, y_train)
    return classifier.predict(X_test)

# Apply Naive Bayes classifier
def naiveBayes(X_train, X_test, y_train):
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    return classifier.predict(X_test)

# Apply decision tree classifier
def decisionTree(X_train, X_test, y_train):
    classifier = DecisionTreeClassifier()
    classifier.fit(X_train, y_train)
    return classifier.predict(X_test)


#Apply randomForest classifier

def randomForest(X_train, X_test, y_train , n_estimators = 10, max_depth = 25, criterion = "gini", min_samples_split = 10):
    classifier = RandomForestClassifier(n_estimators=n_estimators, 
                                        max_depth=max_depth, 
                                        criterion=criterion,
                                        min_samples_split=min_samples_split)
    classifier.fit(X_train, y_train)
    prediction = classifier.predict(X_test)
    return classifier , prediction

