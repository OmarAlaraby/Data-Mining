import numpy as np
from sklearn.metrics import classification_report
from tabulate import tabulate
from colorama import Fore, Style, init

from utils import (
    splitData, load_csv,
    getFeaturesAndLabels,
    fixMissingValues,
    convertNonNumericalData,
    excludeFeatures,
    calculate_performance
)

from classifiers import (
    knn,
    naiveBayes,
    decisionTree,
    randomForest
)

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Excluded features
excludedFeatures = [
    "dbName",
    "avgNumColumns",
    "avgNumRows"
]

def print_colored_report(title, accuracy, precision, recall, confusion_matrix, class_report):
    """
    Prints a classifier report as a table with colors.
    """
    print(f"{Fore.CYAN}{Style.BRIGHT}\n=== {title} ===\n{Style.RESET_ALL}")

    # Table for overall metrics
    metrics_table = [
        ["Accuracy (%)", accuracy],
        ["Precision (%)", precision],
        ["Recall (%)", recall]
    ]
    print(Fore.GREEN + tabulate(metrics_table, headers=["Metric", "Value"], tablefmt="grid"))

    # Print the classification report
    print(Fore.YELLOW + "\nClassification Report:")
    print(tabulate(
        [row.split() for row in class_report.split("\n")[2:-3] if row],
        headers=["Class", "Precision", "Recall", "F1-Score", "Support"],
        tablefmt="grid"
    ))

    # Print the confusion matrix
    print(Fore.MAGENTA + "\nConfusion Matrix:")
    print(tabulate(confusion_matrix, tablefmt="grid"))

def main():
    file_path = 'consistent_classifier_data.csv'
    df = load_csv(file_path)

    # Exclude features and clean data
    excludeFeatures(df, excludedFeatures)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    x, y = df.shape
    K = round(np.sqrt(x))

    # Prepare features and labels
    features, goal = getFeaturesAndLabels(df, 'label')
    target = list(set(goal))
    df = fixMissingValues(df)

    # Split data
    X_train, X_test, y_train, y_test = splitData(features, goal)
    X_train = convertNonNumericalData(X_train)
    X_test = convertNonNumericalData(X_test)

    # KNN Classifier
    y_pred_knn = knn(K, X_train, X_test, y_train)
    A_res, P_res, _, con = calculate_performance(y_test, y_pred_knn)
    knn_report = classification_report(y_test, y_pred_knn, target_names=target, zero_division=0)
    print_colored_report("K-Nearest Neighbors (KNN)", A_res, P_res, P_res, con, knn_report)

    # Naive Bayes Classifier
    y_pred_nb = naiveBayes(X_train, X_test, y_train)
    A_res, P_res, _, con = calculate_performance(y_test, y_pred_nb)
    nb_report = classification_report(y_test, y_pred_nb, target_names=target, zero_division=0)
    print_colored_report("Naive Bayes", A_res, P_res, P_res, con, nb_report)

    # Decision Tree Classifier
    y_pred_dt = decisionTree(X_train, X_test, y_train)
    A_res, P_res, _, con = calculate_performance(y_test, y_pred_dt)
    dt_report = classification_report(y_test, y_pred_dt, target_names=target, zero_division=0)
    print_colored_report("Decision Tree", A_res, P_res, P_res, con, dt_report)

    # Random Forest Classifier
    _, y_pred_rf = randomForest(X_train, X_test, y_train)
    A_res, P_res, _, con = calculate_performance(y_test, y_pred_rf)
    rf_report = classification_report(y_test, y_pred_rf, target_names=target, zero_division=0)
    print_colored_report("Random Forest", A_res, P_res, P_res, con, rf_report)


if __name__ == "__main__":
    main()
