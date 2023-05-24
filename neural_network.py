from joblib import dump, load
from numpy import loadtxt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.neural_network import MLPRegressor


# load the dataset
dataset = pd.read_csv('1000random.csv')
print(dataset.info())

X = dataset.drop(['stars'] , axis =1)

y = dataset.stars

s = StandardScaler()
X = s.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
clf = MLPRegressor(random_state=42, max_iter=5000,hidden_layer_sizes=(100))
clf.fit(X_train, y_train)

test_score = r2_score(y_test, clf.predict(X_test))


print("test set performance: ", test_score)

# Saving model to file
# compress increses save time but lowers file size
dump(clf, 'model.joblib', compress=3) 



