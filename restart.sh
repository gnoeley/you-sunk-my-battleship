#!/bin/sh

dropdb python_getting_started
rm -f db.sqlite3
createdb python_getting_started

if test "$1" == "true"
then
        ./getting-started/bin/python3 manage.py migrate
else
        python3 manage.py migrate
fi

heroku local