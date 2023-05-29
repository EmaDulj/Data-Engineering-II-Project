#predictions on production server
#choosing 5 random repos
#model.joblib pushed from development
#data included

import random
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# load the dataset
dataset = pd.read_csv('fullset_with_more_fields.csv')
for column in dataset.columns:
    dataset = dataset.drop(dataset[dataset[str(column)] == 'ERROR'].index)
dataset['author_type'] = dataset.author_type.apply(lambda x: 1 if x=='User' else 0)


X = dataset.drop(['stars'] , axis =1)
y = dataset.stars

s = StandardScaler()
X = s.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
y = np.array(y_test)

rows_id = random.sample(range(0, X_test.shape[0]-1), 5)

import joblib
model = joblib.load('model.joblib')
print(model.predict(X_test[rows_id]))
print(y[rows_id])
