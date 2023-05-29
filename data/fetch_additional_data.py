import json
import os
import pandas as pd
from datetime import datetime
import re
from sklearn.preprocessing import LabelEncoder
import requests

json_file = open("1000sorted.json", "r", encoding="utf-8")
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
        'has_discussions': [],
        'author_followers': [],
        'author_type': [],
        'contributors': [],
        'commits': [],
        'comments': [],
        'deployments': [],
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
    

file_num = 0

for arr in sh_json:
    file_num += 1
    for item in arr:
        print(item)
        data['size'].append(arr[item]['size'])
        data['stars'].append(arr[item]['stargazers_count'])
        data['forks_count'].append(arr[item]['forks_count'])
        data['open_issues'].append(arr[item]['open_issues'])
        data['has_wiki'].append(arr[item]['has_wiki'])
        data['has_pages'].append(arr[item]['has_pages'])
        data['has_issues'].append(arr[item]['has_issues'])
        data['has_projects'].append(arr[item]['has_projects'])
        data['num_topics'].append(len(arr[item]['topics']))
        data['has_discussions'].append(arr[item]['has_discussions'])
        data['author_type'].append(arr[item]['owner']['type'])

        access_tokens = [] # Add an array of access tokens in here - need atleast 3 tokens 
        
        token = 0

        Get Follower details
        page = 1
        count = 0
        failed_resp = 0
        followers = []
        while (page == 1 or len(followers) == 100) :
            url = arr[item]['owner']['followers_url'] + "?page=" + str(page) + "&per_page=100"
            author_followers_resp = requests.get(url, headers={"Authorization": "Bearer "+ access_tokens[(token % 3)]})
            if (author_followers_resp.status_code == 200) :
                followers = json.loads(author_followers_resp.text)
                count += len(followers)
                page += 1
                print(str(page) + "_" +  str(len(followers)))
            else :
                token += 1
                failed_resp += 1
                print("error - fol")
                if (failed_resp == 5):
                    count = "ERROR"
                    break;
        
        data['author_followers'].append(count)


        page = 1
        count_contributors = 0
        failed_resp = 0
        contributors = []
        while (page == 1 or len(contributors) == 100) :
            url = arr[item]['contributors_url'] + "?page=" + str(page) + "&per_page=100"
            contributors_resp = requests.get(url, headers={"Authorization": "Bearer "+ access_tokens[(token % 4)]})
            if (contributors_resp.status_code == 200) :
                contributors = json.loads(contributors_resp.text)
                count_contributors += len(contributors)
                page += 1
                print(str(page) + "_" +  str(len(contributors)))
            else :
                token += 1
                failed_resp += 1
                print("error - contributors")
                if (failed_resp == 5):
                    count_contributors = "ERROR"
                    break;
        
        data['contributors'].append(count_contributors)

        

        page = 1
        count_commits = 0
        failed_resp = 0
        commits = []
        while (page == 1 or len(commits) == 100) :
            url = arr[item]['commits_url'].replace("{/sha}", "") + "?page=" + str(page) + "&per_page=100"
            commits_resp = requests.get(url, headers={"Authorization": "Bearer "+ access_tokens[(token % 4)]})
            if (commits_resp.status_code == 200) :
                commits = json.loads(commits_resp.text)
                count_commits += len(commits)
                page += 1
                print(str(page) + "_" +  str(len(commits)))
            else :
                token += 1
                failed_resp += 1
                print("error - commits")
                if (failed_resp == 5):
                    count_commits = "ERROR"
                    break;
        
        data['commits'].append(count_commits)

        page = 1
        count_comments = 0
        failed_resp = 0
        comments = []
        while (page == 1 or len(comments) == 100) :
            url = arr[item]['comments_url'].replace("{/number}", "") + "?page=" + str(page) + "&per_page=100"
            comments_resp = requests.get(url, headers={"Authorization": "Bearer "+ access_tokens[(token % 4)]})
            if (comments_resp.status_code == 200) :
                comments = json.loads(comments_resp.text)
                count_comments += len(comments)
                page += 1
                print(str(page) + "_" +  str(len(comments)))
            else :
                token += 1
                failed_resp += 1
                print("error - comments")
                if (failed_resp == 5):
                    count_comments = "ERROR"
                    break;
        
        data['comments'].append(count_comments)

        page = 1
        count_deployments = 0
        failed_resp = 0
        deployments = []
        while (page == 1 or len(deployments) == 100) :
            url = arr[item]['deployments_url'] + "?page=" + str(page) + "&per_page=100"
            deployments_resp = requests.get(url, headers={"Authorization": "Bearer "+ access_tokens[(token % 4)]})
            if (deployments_resp.status_code == 200) :
                deployments = json.loads(deployments_resp.text)
                count_deployments += len(deployments)
                page += 1
                print(str(page) + "_" +  str(len(deployments)))
            else :
                token += 1
                failed_resp += 1
                print("error - deployments")
                if (failed_resp == 5):
                    count_deployments = "ERROR"
                    break;
        
        data['deployments'].append(count_deployments)
        
        
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
        



    df = pd.DataFrame(data= data,columns=['size','stars','forks_count','open_issues','has_wiki','has_pages','has_issues','has_projects', 'has_discussions', 'author_type', 'author_followers', 'contributors', 'commits', 'comments', 'deployments', 'num_topics','javascript','typescript','python','rust','other_language','desc_word_count','created_at','updated_at','pushed_at','has_homepage','license'])

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


    df.to_csv(str(file_num)+'with_more_fields.csv', encoding='utf-8', index=False)
