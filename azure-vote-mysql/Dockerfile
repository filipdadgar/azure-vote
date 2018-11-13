FROM mysql
ADD azurevote.sql /docker-entrypoint-initdb.d
RUN chmod 777 /docker-entrypoint-initdb.d/azurevote.sql