# Store Server

[![Build status](https://github.com/AlexanderObolonkov/store-server/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/AlexanderObolonkov/store-server/actions/workflows/checks.yml)

#### Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev)

## Local Developing
1. Go to the project directory
2. Create and activate a new virtual environment:
   ```bash
   python -m venv ../venv
   . ../venv/bin/activate
   ```
3. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Run migrations, fill the database with the fixture data (optional) etc.:
   ```bash
   ./manage.py migrate
   ./manage.py loaddata <path_to_fixture_files>
   ./manage.py runserver 
   ```
5. Run Redis Server:
   ```bash
   redis-server
   ```
   
6. Run Celery:
   ```bash
   celery -A store worker --loglevel=INFO
   ```

## Production
Deployment in production was based on the [following material](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)