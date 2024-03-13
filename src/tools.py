import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

from scipy.stats import chi2_contingency
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold, train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

from imblearn.ensemble import BalancedRandomForestClassifier, BalancedBaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

RANDOM_STATE = 7

def rename_columns(df, column_name, new_column_name):
    df.rename(columns={column_name: new_column_name}, inplace=True)
    return df


def rename_column_without_prefix(X_train, X_test, prefix=None):
    if prefix is None:
        print("No prefix specified")
        return
    restore_column_name = lambda column: column.replace(prefix, "")
    X_train.rename(columns=restore_column_name, inplace=True)
    X_test.rename(columns=restore_column_name, inplace=True)


def preprocess_dataframe(data):
    data.loc[:, 'DAYS_BIRTH'] = data['DAYS_BIRTH'].map(lambda x: int(-x / 365) if x < 0 else 0)
    data.loc[:, 'DAYS_EMPLOYED'] = data['DAYS_EMPLOYED'].map(lambda x: int(-x / 365) if x < 0 else 0) 
    data = rename_columns(data, 'DAYS_BIRTH', 'AGE')
    data = rename_columns(data, 'DAYS_EMPLOYED', 'YEARS_EMPLOYED')
    data = data.drop(columns=["CODE_GENDER", "CNT_CHILDREN"])
    return data


def show_percentage(plot, crosstab):
    '''
    This function plot percentage proportion in bar plots
    :param plot: plot
    :param crosstab: crosstab information
    '''
    for p in plot.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        percentage = height/crosstab.sum(axis=1) * 100
        if percentage.iloc[0] > 0:
            plot.text(x + width/2, y + height/2, f"{percentage.iloc[0]:.2f}%",
                horizontalalignment='center', verticalalignment='center',
                color='black') 


def generate_confusion_matrix(axes : plt.Axes, matrix : np.ndarray, title=None):
    axes.text(0, 2.3, f"Precision: {(matrix[1][1]/(matrix[1][1]+matrix[0][1])):.3f}") 
    axes.text(1, 2.3, f"Recall: {(matrix[1][1]/(matrix[1][1]+matrix[1][0])):.3f}") 
    axes.xaxis.set_ticklabels(['Predicted Good Customer', 'Predicted Bad Customer'])
    axes.yaxis.set_ticklabels(['Good Customer', 'Bad Customer'])
    if title:
        axes.set_title(title, fontsize=10.5)
    return axes

def print_train_test_confusion_matrix(train_matrix : np.ndarray, test_matrix : np.ndarray, train_title=None, test_title=None):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15, 5))
    sns.heatmap(train_matrix, annot=True, cmap="Greens", fmt='g', ax=ax1)
    ax1 = generate_confusion_matrix(ax1, train_matrix, train_title)

    sns.heatmap(test_matrix, annot=True, cmap="Greens", fmt='g', ax=ax2)
    ax2 = generate_confusion_matrix(ax2, test_matrix, test_title)
    plt.show()

def get_accuracy_from_classification_report(report):
    numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+", report.split("\n")[5])
    return float(numerical_values[0])

def get_info_from_classification_report(report):
    numerical_values_class0 = re.findall(r"[-+]?\d*\.\d+|\d+", report.split("\n")[2])
    numerical_values_class1 = re.findall(r"[-+]?\d*\.\d+|\d+", report.split("\n")[3])
    return float(numerical_values_class0[1]), float(numerical_values_class0[2]), float(numerical_values_class1[1]), float(numerical_values_class1[2])

def get_dict_from_classification_report(report_train, report_test):
    precision_good_cl, recall_good_cl, precision_bad_cl, recall_bad_cl = get_info_from_classification_report(report_train)
    precision_good_cl_test, recall_good_cl_test, precision_bad_cl_test, recall_bad_cl_test = get_info_from_classification_report(report_test)
    return {
        "Train_accuracy": get_accuracy_from_classification_report(report_train), 
        "Test_accuracy": get_accuracy_from_classification_report(report_test), 
        "Train_precision_good_cl": precision_good_cl,
        "Train_recall_good_cl": recall_good_cl,
        "Train_precision_bad_cl": precision_bad_cl,
        "Train_recall_bad_cl": recall_bad_cl,
        "Test_precision_good_cl": precision_good_cl_test,
        "Test_recall_good_cl": recall_good_cl_test,
        "Test_precision_bad_cl": precision_bad_cl_test,
        "Test_recall_bad_cl": recall_bad_cl_test
    }

def perform_logistic_regression(X_train, y_train, X_test, y_test, threshold=0.5, class_weight=None):
    log_reg = LogisticRegression(random_state=RANDOM_STATE, class_weight=class_weight, max_iter=1000)
    log_reg.fit(X_train, y_train)
    y_pred_proba = log_reg.predict_proba(X_train)
    y_pred_train = np.where(y_pred_proba[:,1]>threshold, 1, 0)
    report = classification_report(y_train, y_pred_train)
    accuracy = get_accuracy_from_classification_report(report)
    print("Train Set Accuracy: ", accuracy)
    print(report)
    print("--------------------")

    y_pred_proba = log_reg.predict_proba(X_test)
    y_pred = np.where(y_pred_proba[:,1]>threshold, 1, 0)
    report_test = classification_report(y_test, y_pred)
    accuracy_test = get_accuracy_from_classification_report(report_test)
    print("Test Set Accuracy: ", accuracy_test)
    print(report_test)
    print_train_test_confusion_matrix(train_matrix=confusion_matrix(y_train, y_pred_train), test_matrix=confusion_matrix(y_test, y_pred), 
                           train_title="Train Set\n\n", test_title="Test Set\n\n")
    return log_reg, report, report_test


def chi_squared_test(data, feature1, feature2):
    '''
    This function performs a chi-squared test of independence between two categorical variables
    and prints the p-value of the test.
    :param data: the dataframe containing the features
    :param feature1: the first feature
    :param feature2: the second feature
    '''
    crosstab = pd.crosstab(data[feature1], data[feature2])
    chi2, p, _, _ = chi2_contingency(crosstab)
    print(f"Chi2: {chi2:.2f}, p-value: {p:.2f}")
    if(p < 0.05):
        print(f"Features {feature1} and {feature2} are dependent")
    else:
        print(f"Features {feature1} and {feature2} are independent")