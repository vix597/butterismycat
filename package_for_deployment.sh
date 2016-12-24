#!/bin/sh

# Make sure they're in the directory with django manage.py
if [ ! -f "./manage.py" ];
then
    echo; echo "You're in the wrong directory"; echo
    exit 1
fi

# Make sure the parent directory is for butterismycat
if [ ! -d "../butterismycat" ];
then
    echo; echo "You're in the wrong directory"; echo
    exit 1
fi

staging="/tmp/butterismycat_staging"
package_file="deploy_butterismycat.com.tar.gz"

if [ ! -d $staging ];
then
    #echo "mkdir $staging"
    mkdir $staging
fi

for f in `ls`;
do
    # Copy all the directories except media
    if [ -d $f ];
    then
        if [ ! "$f" = "media" ];
        then
            #echo "cp -R $f $staging"
            cp -R $f $staging
        fi
    fi

    # Copy everything else except the database
    if [ -f $f ];
    then
        if [ ! "$f" = "db.sqlite3" -a ! "$f" = "$package_file" ];
        then
            #echo "cp $f $staging"
            cp $f $staging
        fi
    fi
done

# Tar up the staging directory
#echo "tar -zcvf deploy_butterismycat.com.tar.gz $staging"
tar -zcvf $package_file $staging 

exit 0