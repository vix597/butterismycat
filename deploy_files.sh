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
fi    

exit 0