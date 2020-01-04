# ButterIsMyCat.com

A comic site.

## Running the dev server

1. Setup

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt
```

1. Run tests

```bash
tox -e py37
```

1. Create the superuser

```bash
python3 manage.py createsuperuser
```

1. Run migrations

```bash
python3 manage.py migrate
```

1. Run the dev server

```bash
python3 manage.py runserver
```

## Updating database with changes to the DB models

1. Make migrations

```bash
python3 manage.py makemigrations
```

1. Run `migrate` to actually commit the changes

```bash
python3 manage.py migrate
```
