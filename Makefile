SHELL := /bin/bash

all: pull py restart

pull:
	git pull;

py:
	source .venv/bin/activate; \
    pip install -r requirements.txt; \
    python manage.py migrate; \
    python manage.py collectstatic --noinput; \

restart:
	sudo systemctl restart gunicorn;