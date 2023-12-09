# Epidemiological characterization of rare diseases in Brazil: a study of the Brazilian Rare Diseases Network
[![Python 3.10.0](https://img.shields.io/badge/python-3.10.0-blue.svg)](https://www.python.org/downloads/release/python-3100/)

--- 


## How to reproduce analysis
Setup Python 3.10.0
```bash
sudo apt update
sudo apt upgrade
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xzvf Python-3.10.0.tgz
cd Python-3.10.0
./configure
make
sudo make install
```
Create a virtual environment and install the dependencies :tada: 
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
