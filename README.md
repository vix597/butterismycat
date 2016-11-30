# ButterIsMyCat.com

#### Running the dev server
1. Run tests

```
python3 manage.py test comic
```

1. Create the superuser

```
python3 manage.py createsuperuser
```

1. Run migrations

```
python3 manage.py migrate
```

1. Run the dev server

```
python3 manage.py runserver
```

#### Updating database with changes to the DB models

1. Make migrations

```
python3 manage.py makemigrations comic
```

1. Optionally, look at what will change with `migrate`

```
python3 manage.py sqlmigrate comic <id_from_makemigrations>
```

1. Finally, run `migrate` to actually commit the changes

```
python3 manage.py migrate
```
