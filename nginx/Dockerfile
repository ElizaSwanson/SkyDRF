FROM nginx:latest

RUN mkdir -p /run/nginx && \
    chown -R nginx:nginx /run/nginx && \
    chmod -R 755 /run/nginx && \
    mkdir -p /app/staticfiles && \
    mkdir -p /app/media

# Копируем конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf

# Удаляем директиву user из конфига (если она есть)
RUN sed -i '/^user/d' /etc/nginx/nginx.conf

EXPOSE 80