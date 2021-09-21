FROM ubuntu:18.04

RUN apt-get update
#RUN DEBIAN_FRONTEND=noninteractive TZ=Asia/Singapore apt-get update && apt-get install -y python3-pip apache2 vim libapache2-mod-wsgi-py3
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install python3-pip libapache2-mod-wsgi-py3
RUN pip3 install virtualenv
RUN pip3 install --upgrade pip
ENV PYTHONUNBUFFERED 1
WORKDIR /GuestFacing
COPY requirements.txt /GuestFacing
COPY . /GuestFacing
ADD ./000-default.conf /etc/apache2/sites-available/000-default.conf
RUN chmod 777 /etc/ssl/certs
RUN chmod 777 /etc/ssl/private
ADD ./gtriip-certs/gtriip.crt /etc/ssl/certs
ADD ./gtriip-certs/gtriip.key /etc/ssl/private
ADD ./gtriip-certs/sf_bundle-g2-g1.crt /etc/ssl/certs
RUN chmod 755 /etc/ssl/certs
RUN chmod 710 /etc/ssl/private
ADD ./default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
#RUN a2ensite 000-default.conf
RUN a2enmod ssl
RUN a2ensite default-ssl.conf
RUN chmod 664 /GuestFacing/db.sqlite3
RUN chown :www-data /GuestFacing/db.sqlite3
RUN chown :www-data /GuestFacing
RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod proxy_balancer
RUN a2enmod lbmethod_byrequests
EXPOSE 443
CMD ["apache2ctl", "-D", "FOREGROUND"]