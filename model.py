import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
# Determine features and goal
def determine_features_and_goal(dataFrame):
    features = dataFrame.drop(columns=['label'])
    goal = dataFrame['label']
    return features, goal

# Split data into training and testing
def split_data(features, goal, test_size=0.3, random_state=3):
    X_train, X_test, y_train, y_test = train_test_split(features, goal, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

# Label encode categorical features
def label_encode_categorical_features(dataFrame):
    le = LabelEncoder() # encode non-numircal data into numircal data
    dataFrame = dataFrame.apply(le.fit_transform) # apply the encoder to the data frame
    return dataFrame

# Solve missing values
def solve_missing(dataFrame):
    imputer = SimpleImputer(strategy = "most_frequent") # replace any missing data with the most frequent value
    dataFrame = imputer.fit_transform(dataFrame)
    return dataFrame

# Apply KNN classifier
def apply_knn_classifier(K,X_train, X_test, y_train):
    knn = KNeighborsClassifier(n_neighbors = K)
    knn.fit(X_train, y_train)
    return knn.predict(X_test)

# Apply Naive Bayes classifier
def apply_naive_bayes_classifier(X_train, X_test, y_train):
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    return gnb.predict(X_test)

# Apply decision tree classifier
def apply_decision_tree_classifier(X_train, X_test, y_train):
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    return dt.predict(X_test)


#Apply randomForest classifier

def apply_random_forest_classifier(X_train, X_test, y_train):
    rm = RandomForestClassifier(n_estimators = 10, max_depth = 25, criterion = "gini", min_samples_split = 10)
    rm.fit(X_train, y_train)
    rm_prd = rm.predict(X_test)
    return rm,rm_prd

# Calculate performance using confusion matrix
def calculate_performance(y_test, y_pred):
    confusionMat = confusion_matrix(y_test, y_pred)
    v = round(metrics.accuracy_score(y_test, y_pred) * 100) # compares y_test , y_pred - v = a percantage of similarity 
    w = round(metrics.precision_score(y_test, y_pred, average = 'macro') * 100) # computes the accurecy of the classifier to predict a false postive 
    z = round(metrics.recall_score(y_test, y_pred, average = 'macro') * 100) # computes the percantage of positive labels which the classifier got right
    return v , w , z , confusionMat

if __name__ == '__main__':
    