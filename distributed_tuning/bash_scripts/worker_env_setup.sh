# Update packages
sudo apt-get update -y
sudo apt update -y

# Install python3
sudo apt install python3 python3-pip -y
python3 -m pip install --upgrade pip

# Install python packages
python3 -m pip install numpy
python3 -m pip install pandas
python3 -m pip install scikit-learn
python3 -m pip install jupyter
python3 -m pip install ray[tune]
python3 -m pip install xgboost
python3 -m pip install catboost
python3 -m pip install jupyter



clone the git repository
git clone https://github.com/EmaDulj/Data-Engineering-II-Project.git


ray start --address='<add ip for ray master>:6379'
