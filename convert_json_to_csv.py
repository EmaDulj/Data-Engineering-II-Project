import json
import os
import pandas as pd
from datetime import datetime
import re
from sklearn.preprocessing import LabelEncoder


json_file = open("1000random.json", "r", encoding="utf-8")
sh_json = json.load(json_file)
json_file.close()
data = {'size': [],
        'stars':[],
        'forks_count':[],
        'open_issues':[],
        'has_wiki':[],
        'has_pages':[],
        'has_issues':[],
        'has_projects':[],
        'num_topics':[],
        'javascript':[],
        'typescript':[],
        'python':[],
        'other_language':[]

        }
def check_language(language):
    if language == 'JavaScript':
        data['javascript'].append(1)  
        data['typescript'].append(0)
        data['python'].append(0) 
        data['other_language'].append(0)
    elif language == 'TypeScript':  
        data['typescript'].append(1) 
        data['javascript'].append(0) 
        data['python'].append(0) 
        data['other_language'].append(0)
    elif language == 'Python':
        data['python'].append(1) 
        data['javascript'].append(0) 
        data['typescript'].append(0)
        data['other_language'].append(0)
    else:
        data['other_language'].append(1)
        data['javascript'].append(0)  
        data['typescript'].append(0)
        data['python'].append(0) 


for item in sh_json['items']:
    data['size'].append(item['size'])
    data['stars'].append(item['stargazers_count'])
    data['forks_count'].append(item['forks_count'])
    data['open_issues'].append(item['open_issues'])
    data['has_wiki'].append(item['has_wiki'])
    data['has_pages'].append(item['has_pages'])
    data['has_issues'].append(item['has_issues'])
    data['has_projects'].append(item['has_projects'])
    data['num_topics'].append(len(item['topics']))
    check_language(item['language'])



df = pd.DataFrame(data= data,columns=['size','stars','forks_count','open_issues','has_wiki','has_pages','has_issues','has_projects','num_topics'])




df.to_csv('1000random.csv', encoding='utf-8', index=False)