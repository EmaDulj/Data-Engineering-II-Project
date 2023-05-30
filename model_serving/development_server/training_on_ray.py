from joblib import dump, load
from numpy import loadtxt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
import ray
import time
from ray.util.joblib import register_ray

ray.init()
register_ray()

dataset = pd.read_csv('fullset_with_more_fields.csv')
for column in dataset.columns:
    dataset = dataset.drop(dataset[dataset[str(column)] == 'ERROR'].index)
dataset['author_type'] = dataset.author_type.apply(lambda x: 1 if x == 'User' else 0)

X = dataset.drop(['stars'], axis=1)

y = dataset.stars

s = StandardScaler()
X = s.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)


start_time = time.time()

@ray.remote
def train_model(X, y):
    clf = RandomForestRegressor(n_jobs=-1, n_estimators=190, random_state=42)
    clf.fit(X, y)
    return clf

clf = train_model.remote(X_train, y_train)
clf = ray.get(clf)


elapsed_time = time.time() - start_time

test_score = r2_score(y_test, clf.predict(X_test))

print("Test set performance:", test_score)
print("Elapsed time: %.2f seconds" % elapsed_time)
