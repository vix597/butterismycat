#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***ERROR: Please run ./setup_site.sh first.***"; echo
    exit 1
fi

python3 manage.py --production migrate
python3 manage.py --production runserver

exit 0