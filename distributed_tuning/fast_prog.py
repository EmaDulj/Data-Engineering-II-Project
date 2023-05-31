import numpy as np
import pandas as pd
# importing libraries
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from numpy import percentile
from sklearn.model_selection import train_test_split

data = pd.read_csv("/Data_engineering-II-Project/data/fullset_with_more_fields.csv")

print(data.head())

from sklearn.preprocessing import StandardScaler
#,  
columns_to_keep = ['mit_license', 'nan_license', 'apache_license', 'other_license', 'remain_license', 'comments', 'num_topics', 'has_homepage', 'size','forks_count', 'open_issues', 'contributors', 'commits', 'updated_at', 'created_at' ]

# Filter the DataFrame using the loc accessor
X = data.loc[:, columns_to_keep]

columns_to_keep_label = ['stars']

# Filter the DataFrame using the loc accessor
y = data['stars']

q25, q75 = percentile(y, 25), percentile(y, 75)
iqr = q75 - q25
# calculate the outlier cutoff
cut_off = iqr * 3
lower, upper = q25 - cut_off, q75 + cut_off

outliers = [x for x in y if x < lower or x > upper]
print('Identified outliers: %d' % len(outliers))
# identify outliers
outliers_idx = [x < lower or x > upper for x in y]
outliers = pd.Series(outliers_idx)

new_data = data[~outliers.values]

X = new_data.loc[:, columns_to_keep]
y = new_data['stars']

s = StandardScaler()
X = s.fit_transform(X)


X_train_scaled, X_test_scaled, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=42)


import ray
from ray import tune

ray.init(num_cpus=1)

def train_model(config):

    model = xgb.XGBRegressor(
        n_estimators= config["n_estimators"] , 
        max_depth= config["max_depth"], 
        max_leaves= config["max_leaves"], 
        learning_rate=config["learning_rate"], 
        booster=config["booster"], #'RMSE' 
        grow_policy = config["grow_policy"],
        reg_alpha = config["reg_alpha"],
        #objective = config["objective"],
        use_best_model=True)
    
    model.fit(X_train_scaled, y_train)

    y_train_pred  =  model.predict(X_train_scaled)
    y_pred = model.predict(X_test_scaled)

    train_score = r2_score(y_train , y_train_pred)
    r2 = r2_score(y_test, y_pred)
    
    tune.report(accuracy=r2)
    


    
# Define the search space
config = {
    "n_estimators": tune.choice([500, 100, 200, 300, 400]),
    "max_depth": tune.choice([8, 10, 12]),
    "max_leaves": tune.choice([10, 20, 5, 25]),
    "learning_rate": tune.choice([0.1, 0.05, 0.3, 0.2]),
    "booster": tune.choice(["gbtree", "dart"]),
    "grow_policy": tune.choice(['depthwise', 'lossguide']),
    "reg_alpha": tune.choice([0.1, 0.05])
    #"objective": tune.choice(["reg:squarederror", "reg:linear", "reg:gamma", "reg:poisson", "reg:tweedie"])
}

# Configure Ray Tune
tune_config = {
    "num_samples": 40,
    "config": config,
    "mode": "max",
#    "search_alg": tune.suggest.BasicVariantGenerator(),
#     "stop": {"training_iteration": 10}
}

# Run the hyperparameter search
analysis = tune.run(train_model, **tune_config)

# Get the best configuration and its corresponding accuracy
best_config = analysis.get_best_config(metric="accuracy")
best_accuracy = analysis.get_best_trial(metric="accuracy").last_result["accuracy"]

print("Best configuration:", best_config)
print("Best accuracy:", best_accuracy)



