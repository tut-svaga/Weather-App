FROM nginx:alpine
# Копируем наш конфиг поверх дефолтного
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Копируем файлы фронта
COPY . /usr/share/nginx/html

EXPOSE 10000
CMD ["nginx", "-g", "daemon off;"]