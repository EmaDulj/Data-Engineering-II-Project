#!/usr/bin/bash

while read oldrev newrev ref
do
	if [[ $ref =~ .*/master$ ]];
	then
		echo "Master ref received. Deploying master branch to production..."
		sudo git --work-tree=/application_group12/model_serving/production_server --git-dir=/home/appuser/application_group12 checkout -f
	else
		echo "Ref $ref successfully received. Doing nothing: only the master branch may be deployed on this server."
fi
done
