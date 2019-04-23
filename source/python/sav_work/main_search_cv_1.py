import os
import time
import numpy as np
import pandas as pd
import scipy.io as sio
import sklearn.svm as svm
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

# global variable
# C = 4
# gamma = 0.02
test_size = 0.33
split_random_state = 1
# model = svm.SVC(kernel='rbf', gamma=gamma, C=C)

# Усечение сигнала слева и справа
left_cup, right_cup, cup_flag = 100, 70, False

# Выбор классов
# classes = '0, 1, 4, 5, 7'
# classes = '0, 1, 4, 6, 7'
classes = '0, 1, 4, 7, 9'
# classes = '0, 1, 2, 3, 4, 5, 6, 7, 8, 9'

file_name_data_set = '../data/data10mov_no_abs.mat'

qt = QuantileTransformer()

# test global variable
search_random_state = 10
svc = svm.SVC(kernel='rbf')
parameters = {
    'C': np.arange(0.5, 5.1, 0.5),
    'gamma': np.arange(0.01, 0.5, 0.01)
}

# clf = GridSearchCV(svc, parameters, cv=5, iid=False)
clf = RandomizedSearchCV(svc, parameters, cv=5, iid=False,
                         random_state=search_random_state)


def read_mat(file_name):
    mat = sio.loadmat(file_name)
    data = pd.Series([value[0] for value in mat['data']], [
        'Кисть вверх',                  # 0
        'Кисть вниз',                   # 1
        'Сжатие всех пальцев',          # 2
        'Сжатие указ пальца',           # 3
        'Сжатие среднего пальца',       # 4
        'Сжатие безымянного пальца',    # 5
        'Щелчок большого с средним',    # 6
        'Разжимание всех пальцев',      # 7
        'Поворот кисти влево',          # 8
        'Поворот кисти вправо'          # 9
    ])
    return data


def train(X_train, y_train, quantile_transform=True):
    if quantile_transform:
        X_train = qt.fit_transform(X_train)
    clf.fit(X_train, y_train)
    return clf.score(X_train, y_train)


def test(X_test, y_test, quantile_transform=True):
    if quantile_transform:
        X_test = qt.transform(X_test)
    return clf.score(X_test, y_test)


def main():
    emg_data_set = read_mat(os.path.abspath(file_name_data_set))

    classes_list = list(map(int, classes.split(",")))

    X, y = [], []
    for index, value in enumerate(emg_data_set):
        if not (index in classes_list):  # optional
            continue

        X.extend(value)
        y.extend([index] * len(value))

    if cup_flag:                                          # optional
        for index, value in enumerate(X):
            X[index] = value[left_cup:-right_cup]

    start_time = time.time()                            # time begin (optional)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=split_random_state)

    train_results = train(X_train, y_train)
    tests_results = test(X_test, y_test)

    print(f"Time: {time.time() - start_time} seconds")  # time end (optional)

    print(f"Train result: {train_results:.2%}")
    print(f"Verification result: {tests_results:.3%}")

    print(f"\nWarning! cup_flag = {cup_flag}")


if __name__ == '__main__':
    main()