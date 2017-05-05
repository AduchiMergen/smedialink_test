FROM python:3
EXPOSE 8000
COPY requirements.txt /srv
RUN pip install -r /srv/requirements.txt
WORKDIR /srv
COPY manage.py /srv
COPY templates /srv/templates
COPY smedialink_test /srv/smedialink_test
COPY partymaker /srv/partymaker
RUN ./manage.py migrate
CMD ./manage.py runserver 0.0.0.0:8000
