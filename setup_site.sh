#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***Create new venv***"; echo
    virtualenv --system-site-packages ./venv 
    source ./venv/bin/activate

    # Only upgrade on initial setup.
    pip3 install -r requirements.txt --upgrade
fi

python3 manage.py collectstatic

if [ ! -d "/home/public/butterismycat/media" ];
then
    mkdir /home/public/butterismycat/media
    chmod a+w /home/public/butterismycat/media
fi    

if [ ! -d "/home/protected/database" ];
then
    mkdir /home/protected/database
    chmod a+w /home/protected/database
fi

python3 manage.py migrate

if [ -f "/home/protected/database/db.sqlite3" ];
then
    chmod a+w /home/protected/database/db.sqlite3
else
    echo "ERROR: Could not modify permission on db file"
    exit 1
fi

exit 0