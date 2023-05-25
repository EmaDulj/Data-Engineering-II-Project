from joblib import dump, load
from numpy import loadtxt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor

# load the dataset
#dataset = pd.read_csv('with_author_details.csv')
#dataset['author_type'] = dataset.author_type.apply(lambda x: 1 if x=='User' else 0)
#dataset = pd.read_csv('1000random_updated.csv',index_col=0)
dataset = pd.read_csv('1000random.csv')
print(dataset.info())

#X = dataset.drop(['stars','author_type','has_pages','has_wiki'] , axis =1)
X = dataset.drop(['stars'] , axis =1)

y = dataset.stars

s = StandardScaler()
X = s.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
clf = RandomForestRegressor(n_jobs=-1, n_estimators=200, verbose=1, random_state=42)
clf.fit(X_train, y_train)

test_score = r2_score(y_test, clf.predict(X_test))


print("test set performance: ", test_score)

# Saving model to file
# compress increses save time but lowers file size
dump(clf, 'model.joblib', compress=3) 




