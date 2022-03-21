FROM linuxconfig/lemp
COPY armbook_packaged/ /var/www/html/
COPY Certificate.crt /etc/nginx/
COPY Key.key /etc/nginx/
COPY default /etc/nginx/sites-enabled/
EXPOSE 443