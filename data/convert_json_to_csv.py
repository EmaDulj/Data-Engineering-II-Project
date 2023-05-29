import json
import os
import pandas as pd
from datetime import datetime
import re
from sklearn.preprocessing import LabelEncoder


json_file = open("1000sorted.json", "r", encoding="utf-8")
sh_json = json.load(json_file)
json_file.close()
data = {'stars':[],
        'size': [],
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
        'rust':[],
        'other_language':[],
        'desc_word_count':[],
        'created_at':[],
        'updated_at':[],
        'pushed_at':[],
        'has_homepage':[],
        'license':[]
        }
def check_language(language):
    langs = ['JavaScript','TypeScript','Python','Rust']
    data['javascript'].append(language == 'JavaScript')      
    data['typescript'].append(language == 'TypeScript')    
    data['python'].append(language == 'Python') 
    data['rust'].append(language == 'Rust')   
    data['other_language'].append(language not in langs) 
    

for arr in sh_json:
    for item in arr:
        data['size'].append(arr[item]['size'])
        data['stars'].append(arr[item]['stargazers_count'])
        data['forks_count'].append(arr[item]['forks_count'])
        data['open_issues'].append(arr[item]['open_issues'])
        data['has_wiki'].append(arr[item]['has_wiki'])
        data['has_pages'].append(arr[item]['has_pages'])
        data['has_issues'].append(arr[item]['has_issues'])
        data['has_projects'].append(arr[item]['has_projects'])
        data['num_topics'].append(len(arr[item]['topics']))
        check_language(arr[item]['language'])
        
        if arr[item]['description'] != None:
            res = len(arr[item]['description'].split())
        else:
            res = 0
        data['desc_word_count'].append(res)
        data['created_at'].append(arr[item]['created_at'])
        data['pushed_at'].append(arr[item]['pushed_at'])
        data['updated_at'].append(arr[item]['updated_at'])
        data['has_homepage'].append(arr[item]['homepage'])

        if arr[item]['license'] != None:
            data['license'].append(arr[item]['license']['name'])
        else:
            data['license'].append(None)
        



df = pd.DataFrame(data= data,columns=['stars','size','forks_count','open_issues','has_wiki','has_pages','has_issues','has_projects','num_topics','javascript','typescript','python','rust','other_language','desc_word_count','created_at','updated_at','pushed_at','has_homepage','license'])

time_columns = ['created_at','updated_at','pushed_at']
for column in time_columns:
    df[column] = df[column].apply(lambda x : x.replace('T',' ').replace('Z',''))
    df[column] = df[column].apply(lambda x: int(datetime.strptime(x,'%Y-%m-%d %H:%M:%S').timestamp() / (60*60)))
df['has_homepage'] = df['has_homepage'].fillna('')
df['has_homepage'] = df['has_homepage'].apply(lambda x : 1 if len(x) > 0 else 0)
licenses = ['mit_license','nan_license','apache_license','other_license','remain_license']
df['license'] = df['license'].fillna('')

for i in licenses:
    if i.startswith('mit'):
        df[i] = df['license'].apply(lambda x: 1 if x == 'MIT License' else 0)
    elif i.startswith('nan'):
        df[i] = df['license'].apply(lambda x: int(len(x) == 0))
    elif i.startswith('apache'):
        df[i] = df['license'].apply(lambda x: 1 if x == 'Apache License 2.0' else 0)
    elif i.startswith('other'):
        df[i] = df['license'].apply(lambda x: 1 if x == 'Other' else 0)    

df['remain_license'] = (df[licenses[:-1]].sum(axis=1) == 0).astype(int)
df = df.drop('license',axis=1)


df.to_csv('1000random.csv', encoding='utf-8', index=False)