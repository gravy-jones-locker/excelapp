sudo apt-get -y update

sudo apt-get -y install build-essential
sudo apt-get -y install python3-dev python3-venv python3-pip
sudo apt-get -y uwsgi nginx uwsgi-plugin-python3

# Change this to wherever you want everything to be
mkdir /home/disney
cd /home/disney

python3 -m venv venv
source venv/bin/activate

pip3 install --upgrade pip
pip3 install wheel
pip3 install django
pip3 install pandas
pip3 install xlrd
pip3 install openpyxl
pip3 install xlsxwriter

mkdir logs
mkdir excelapp

cd excelapp
git clone https://github.com/gravy-jones-locker/excelapp.git .

# !! edit for setup-specific ip details
sudo cp server/django /etc/nginx/sites-enabled/django

# !! edit for setup-specific directories
sudo cp server/django.ini /etc/uwsgi/apps-enabled/django.ini

# !! edit for setup-specific directories
sudo cp _config.py config.py

# !! edit for setup-specific ip details
sudo cp excelapp/_settings.py excelapp/settings.py

sudo mkdir webapp/static/input
sudo mkdir webapp/static/output

python3 manage.py migrate

sudo chown ubuntu -R /home/disney

sudo service nginx restart
sudo service uwsgi restart