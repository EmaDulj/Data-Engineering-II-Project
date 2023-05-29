from celery import Celery
from joblib import dump, load
from numpy import loadtxt
import numpy as np
import pandas as pd 
model_file = './model.joblib'
data_file = './data.csv'

def load_data():
    dataset = pd.read_csv(data_file)
    for column in dataset.columns:
        dataset = dataset.drop(dataset[dataset[str(column)] == 'ERROR'].index)
    dataset['author_type'] = dataset.author_type.apply(lambda x: 1 if x=='User' else 0)
    X = dataset.drop(['stars'] , axis =1)
    y = dataset.stars
    return X, y

def load_model():
    loaded_clf = load('model.joblib') 
    return loaded_clf

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task
def get_predictions():
    results ={}
    X, y = load_data()
    loaded_model = load_model()
    predictions = np.round(loaded_model.predict(X)).flatten().astype(np.int32)
    results['y'] = y.tolist()
    results['predicted'] = predictions.tolist()
    return results

@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()

    score = loaded_model.score(X, y)
    return f"{score*100:.2f}%"

if __name__ == "__main__":
    get_accuracy()
