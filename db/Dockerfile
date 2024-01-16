FROM mysql:latest

# Environment variables
#ENV MYSQL_ROOT_PASSWORD=root_password
#ENV MYSQL_DATABASE=PostDB
#ENV MYSQL_USER=db_user
#ENV MYSQL_PASSWORD=db_password

COPY init.sql /docker-entrypoint-initdb.d/init.sql

# port
EXPOSE 3306

CMD ["mysqld"]
