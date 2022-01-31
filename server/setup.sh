sudo apt-get -y update

sudo apt-get -y install build-essential
sudo apt-get -y install python3-dev python3-venv python3-pip
sudo apt-get -y libapache2-mod-wsgi-py3

# Change this to wherever you want everything to be
mkdir ~/morpheus
cd ~/morpheus

python3 -m venv venv
source venv/bin/activate

pip3 install --upgrade pip
pip3 install wheel
pip3 install openpyxl
pip3 install django
pip3 install pandas

git clone https://github.com/gravy-jones-locker/excelapp.git

# !! edit for setup-specific directories
cp _config.py config.py

# !! edit for setup-specific ip details
cp excelapp/_settings.py excelapp/settings.py

mkdir excelapp/webapp/static/input
mkdir excelapp/webapp/static/output

python3 manage.py migrate

sudo chmod a+wrx -R ~/morpheus
sudo chmod a+wrx -R /etc/apache2/httpd.conf