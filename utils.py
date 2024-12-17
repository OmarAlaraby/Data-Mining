import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix
from sklearn import metrics


def load_csv(filePath):
    dataFrame = pd.read_csv(filePath)
    return dataFrame


def excludeFeatures(dataFrame , excluded) :
    dataFrame.drop(columns=excluded)


#  Determine features and goal
def getFeaturesAndLabels(dataFrame , label):
    features = dataFrame.drop(columns=label)
    goal = dataFrame[label]
    return features, goal


# Split data into training and testing
def splitData(features, goal, test_size=0.5, random_state=3):
    X_train, X_test, y_train, y_test = train_test_split(features, goal, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

# Label encode categorical features
def convertNonNumericalData(dataFrame):
    encoder = LabelEncoder() # encode non-numircal data into numircal data
    dataFrame = dataFrame.apply(encoder.fit_transform) # apply the encoder to the data frame
    return dataFrame

# Solve missing values
def fixMissingValues(dataFrame):
    imputer = SimpleImputer(strategy = "most_frequent") # replace any missing data with the most frequent value
    dataFrame = imputer.fit_transform(dataFrame)
    return dataFrame

# Calculate performance using confusion matrix
def calculate_performance(y_test, y_pred):
    confusionMat = confusion_matrix(y_test, y_pred)
    accuracy = round(metrics.accuracy_score(y_test, y_pred) * 100) # compares y_test , y_pred - v = a percantage of similarity 
    precision = round(metrics.precision_score(y_test, y_pred, average = 'macro' , zero_division=0) * 100) # computes the accurecy of the classifier to predict a false postive 
    recall = round(metrics.recall_score(y_test, y_pred, average = 'macro' ,zero_division=0) * 100 ) # computes the percantage of positive labels which the classifier got right
    return accuracy , precision , recall , confusionMat

