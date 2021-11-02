FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install python3-pip libapache2-mod-wsgi-py3
RUN pip3 install virtualenv
RUN pip3 install --upgrade pip
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /GuestFacing
COPY requirements.txt /GuestFacing
RUN pip install -r requirements.txt
COPY . /GuestFacing
ADD ./000-default.conf /etc/apache2/sites-available/000-default.conf
RUN a2ensite 000-default.conf
RUN chmod 775 /GuestFacing
RUN chmod 777 /GuestFacing/logs
RUN chmod 777 /GuestFacing/logs/info.log
RUN chmod 777 /GuestFacing/media
RUN chmod 777 /GuestFacing/static/CACHE
RUN chmod 777 /GuestFacing/static/CACHE/css
RUN chmod 664 /GuestFacing/db.sqlite3
RUN chown :www-data /GuestFacing/db.sqlite3
RUN chown :www-data /GuestFacing
RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod proxy_balancer
RUN a2enmod lbmethod_byrequests
EXPOSE 80 443
CMD ["apache2ctl", "-D", "FOREGROUND"]