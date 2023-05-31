import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns

# Configure visualisations
%matplotlib inline
color = sns.color_palette()
pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999
# mpl.style.use( 'ggplot' )
sns.set_style( 'whitegrid' )
pylab.rcParams[ 'figure.figsize' ] = 10,8
seed = 7

# importing libraries
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor

from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
from numpy import percentile

np.random.seed(seed)

# Compute the correlation matrix
correlation_matrix = data.corr()

# Plot the correlation matrix using a heatmap
plt.figure(figsize=(20, 20))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

#'mit_license', 'nan_license', 'apache_license', 'other_license', 'remain_license', 'num_topics',   'has_homepage', 'size', , 'updated_at', 'created_at'

columns_to_keep = ['forks_count', 'commits', 'open_issues', 'comments', 'author_type', 'updated_at', 'created_at']

# Filter the DataFrame using the loc accessor
X = data.loc[:, columns_to_keep]

columns_to_keep_label = ['stars']

# Filter the DataFrame using the loc accessor
y = data['stars']

q25, q75 = percentile(y, 25), percentile(y, 75)
iqr = q75 - q25
# calculate the outlier cutoff
cut_off = iqr * 1.5
lower, upper = q25 - cut_off, q75 + cut_off

# identify outliers
outliers = [x for x in y if x < lower or x > upper]
print('Identified outliers: %d' % len(outliers))
# identify outliers index
outliers_idx = [x < lower or x > upper for x in y]
outliers = pd.Series(outliers_idx)

#Filter and remove outliers
new_data = data[~outliers.values]

X = new_data.loc[:, columns_to_keep]
y = new_data['stars']

# Scale data
s = StandardScaler()
X = s.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, shuffle=True, random_state=42)


reg = GradientBoostingRegressor(verbose = 1, n_estimators = 100)
reg.fit(X_train , y_train)

training_score = reg.score(X_train, y_train)
test_score = reg.score(X_test, y_test)

print("training set performance: ", training_score)
print("test set performance: ", test_score)

pred = reg.predict(X_test).astype(int)

temp1 = y_test.values > 0
plt.scatter(y_test.values[temp1], pred[temp1])
plt.xlabel("original", fontsize=12)
plt.ylabel("predictions", fontsize=12)
plt.show()


model = CatBoostRegressor(iterations= 200 , depth= 12 , learning_rate= 0.2 , loss_function='RMSE' , use_best_model=True)
model.fit(X_train, y_train, eval_set=(X_test,y_test),plot=True)

y_train_pred  =  model.predict(X_train)
y_pred = model.predict(X_test)

train_score = r2_score(y_train , y_train_pred)
test_score = r2_score(y_test, y_pred)

print("Training score - " + str(train_score))
print("Test score - " + str(test_score))
