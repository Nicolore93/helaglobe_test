FROM nginx:alpine
# Copia i certificati nel container
COPY ./config/default.conf /etc/nginx/conf.d/default.conf
# COPY ./index.html /usr/share/nginx/html/index.html

CMD ["nginx", "-g", "daemon off;"]