FROM    tiangolo/uwsgi-nginx-flask:python3.6

RUN     apt-get update && \
        apt-get install default-libmysqlclient-dev -y && \
        pip install flask-mysql
 
ADD     /azure-vote /app
RUN chmod -R 755 /app/static/
RUN chmod -R 755 /app/templates/