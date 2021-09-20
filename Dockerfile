FROM ubuntu:18.04

RUN apt-get update && \
	apt-get install -y apt-utils vim curl apache2 apache2-utils && \
	apt-get -y install python3-pip libapache2-mod-wsgi-py3 && \
	pip3 install virtualenv && \
	pip3 install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE 1 && \
	PYTHONUNBUFFERED 1
WORKDIR /GuestFacing
COPY . /GuestFacing
RUN virtualenv sc-env && \
	source sc-env/bin/activate \
	pip3 install -r requirements.txt && \
	python3 manage.py migrate && \
	python3 manage.py makemigrations && \
	python3 manage.py collectstatic --noinput && \
	chmod 777 /etc/ssl/certs && \
	chmod 777 /etc/ssl/private
ADD ./gtriip-certs/gtriip.crt /etc/ssl/certs
ADD ./gtriip-certs/gtriip.key /etc/ssl/private
ADD ./gtriip-certs/sf_bundle-g2-g1.crt /etc/ssl/certs
RUN chmod 755 /etc/ssl/certs && \
	chmod 710 /etc/ssl/private
ADD ./default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
#RUN a2ensite 000-default.conf
RUN a2enmod ssl && \
	a2ensite default-ssl.conf && \
	chmod 664 /GuestFacing/db.sqlite3 && \
	chown :www-data /GuestFacing/db.sqlite3 && \
	chown :www-data /GuestFacing && \
	a2enmod proxy && \
	a2enmod proxy_http && \
	a2enmod proxy_balancer && \
	a2enmod lbmethod_byrequests
EXPOSE 443
CMD ["apache2ctl", "-D", "FOREGROUND"]
