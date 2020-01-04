#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***Create new venv***"; echo
    python3 -m venv ./venv
    source ./venv/bin/activate

    # Only upgrade on initial setup.
    pip install -r requirements.txt
fi

python3 manage.py --production collectstatic

if [ ! -d "/home/public/butterismycat/media" ];
then
    mkdir /home/public/butterismycat/media
    chgrp web /home/public/butterismycat/media
fi

if [ ! -d "/home/protected/database" ];
then
    mkdir /home/protected/database
    chgrp web /home/protected/database
    chmod g+w /home/protected/database
fi

python3 manage.py --production migrate

if [ -f "/home/protected/database/db.sqlite3" ];
then
    chgrp web /home/protected/database/db.sqlite3
    chmod g+w /home/protected/database/db.sqlite3
else
    echo "ERROR: Could not modify permission on db file"
    exit 1
fi

exit 0