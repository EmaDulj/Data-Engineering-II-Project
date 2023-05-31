# Data-Engineering-II-Project

In this project we analysed what features should a GitHub repository have in order to have a big number of stars, or in other words, to be popular. We worked on finding the most accurate model for predicting the number of stars for a GitHub repository with more than fifty stars while focusing on providing a scalable CI/CD environment that can be used as a big data application.

We collected data from the GitHub REST API. As can be seen in the "data" folder, we merged 10 smaller datasets consisting of 100 repos (due to pagination). In the folder there are other sizes available for testing purposes. We used "fullset_with_more_fields.csv" that was made by adding more features to "1000sorted.json" by fetching additional data from URLs.

For the deployment of the model on our clien VM we have files from scripts/ansible folder and we have run "start_instances.py" to start two more VMs: on for the development server and one for the production server. In order to login to these servers, a SSH key was generated and Ansible hosts file was updated. 

We used Git Hooks to push files from the development server to the production. In order to use this we created a Git Hook post-receive file in a git empty directory.

On the development server ("model_serving/development_server") we have evaluated a couple of models, choose the best one (Random Forest) and trained it on parallel by having a Ray cluster ("training_on_ray.py"). The head was on the development server and we started two additional workers. You can see all the needed Ray documentation here https://docs.ray.io/en/latest/cluster/vms/user-guides/launching-clusters/on-premises.html#on-prem. After training the trained model ("model.joblib" file) is pushed to the production server. 

On the production server ("model_serving/production_server") are all the files for a Flask based web application as a frontend server and a Celery and RabbitMQ server for backend server. There is also the pushed model and the data set, as well as the code for running the predictions for 5 repositories. We have added "nginx.conf" to manage the requests for the application. 

Instructions for data fetching from URL Links:
To run the data collection scripts you need to add github PAT to the right place.
The script is automated to switch between multiple tokens to avoid distruptions due to request limitations.
Add atleast 3 tokens to the array for better performance - and change the number of tokens parameter appropriately.

Instructions to run distributed hyper-parameter tuning:
Use the sh file in distributed tuning folder to set up the VM annd install all necessary packages.
Change the IP to connect to the ray master node. Change the number of CPU as necessary. Start VM by VM and do the scalability tests.
