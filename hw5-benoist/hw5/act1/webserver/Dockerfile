FROM linuxconfig/lemp
COPY ./armbook/ /etc/nginx
COPY ./Certificate.crt /etc/nginx/
COPY ./Key.key /etc/nginx/
COPY ./default.conf /etc/nginx/sites-enabled/default
EXPOSE 443
