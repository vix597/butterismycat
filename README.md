# ButterIsMyCat.com

#### Running the dev server

__Run The dev server with defaults__

```
python manage.py runserver
```

__Run the dev server on localhost port 8080__

```
python manage.py runserver 8080
```

__Run the dev server on all interfaces on port 8080__

```
python manage.py runserver 0.0.0.0:8080
```

#### Setting up the database

```
python manage.py migrate
```

#### Updating database with changes to the DB models

1. Using the `comic` app as an example, Run `makemigrations` to create the changes

```
python manage.py makemigrations comic

Output:
Migrations for 'comic':
  comic/migrations/<id>_initial.py:
    - some info here
    - ...
```

1. Make note of `<id>` above and run `sqlmigrate` to see what changes will be made once we migrate

```
python manage.py sqlmigrate comic <id>
```

1. Finally, run `migrate` to actually commit the changes shown in the output from the last command to the database

```
python manage.py migrate
```

#### Playing with the api in a shell

1. Using the `comic` app as an example, run:

```
python manage.py shell
```

1. Once in the shell, run:

```
>>> from comic.models import Comic 
>>> Comic.objects.all()
<QuerySet []>
>>>
```

1. Now you can mess around with the API