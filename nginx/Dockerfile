FROM nginx:latest

RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/media && \
    chown -R nginx:nginx /run && \
    chmod -R 755 /run

COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80