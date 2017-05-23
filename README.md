PaperLIMS
=========

Not Quite Ready!!!

Naturally feel free to look around though.


Setup
-----

Create the virtual environment

```
python3 -m venv ./
```

Now activate for every step below (even the historical)

```
. bin/activate
```

Historical
----------

The following is how the PaperLIMS Django application was created.

Create base pip requirments file

*remove the ==VERSION.NUMBER if you want the latest and greatest*

```
echo "Django==1.11.1" >> requirements.txt
echo "XlsxWriter==0.9.6" >> requirements.txt
echo "argparse==1.4.1" >> requirements.txt
echo "django-widget-tweaks==1.4.1" >> requirements.txt
echo "psycopg2==2.7.1" >> requirements.txt
echo "pytz==2017.2" >> requirements.txt
echo "xlrd==1.0.0" >> requirements.txt
```

Install these reqs

```
pip install -r requirements.txt
```

Create the project

```
django-admin startproject paperlims
```

Now create the core app

```
cd paperlims
./manage.py startapp core
```

Create the Postgres DB

if using a local Postgres database

```
psql -f db/init_db.sql
```

You should be able to connect like so

*default password is __nodeadtrees__*

```
psql -U paperplane paperlims -P
```


Initialize DB
-------------

```
./manage migrate
```

Create superuser

*I typically use __admin:justusepaper__*

```
./manage.py createsuperuser
Username (leave blank to use 'slohr'): admin
Email address: admin@dev.null
Password: 
Password (again): 
Superuser created successfully.
```
