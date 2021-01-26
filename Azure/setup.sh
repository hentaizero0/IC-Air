#!/bin/bash

sudo apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc -y

sudo cp freetds.conf . /etc/freetds/
sudo cp odbcinst.ini . /etc/
sudo cp odbc.ini . /etc

sudo pip3 install pyodbc
