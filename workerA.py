from celery import Celery
from joblib import dump, load
from numpy import loadtxt
import numpy as np
from sklearn.ensemble import RandomForestClassifier


model_file = './model.joblib'
data_file = './data.csv'

def load_data():
    dataset =  loadtxt(data_file, delimiter=',')
    X = dataset.drop(['stars'] , axis =1)
    y = dataset.stars
    return X, y

def load_model():
    # load json and create model
    loaded_clf = load('model.joblib') 
    #print("Loaded model from disk")
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


    #print ('results[y]:', results['y'])
    # for i in range(len(results['y'])):
        #print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
        # results['predicted'].append(predictions[i].tolist()[0])
    #print ('results:', results)
    return results

@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()

    score = loaded_model.score(X, y)
    #print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
    return score[1]*100

