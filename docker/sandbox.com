server {
  listen 80;
  server_name 0.0.0.0;

  root /var/www/html/;
  index index.html index.htm;

  client_max_body_size 100M;

  location /browser/ {
    proxy_pass http://127.0.0.1:8081/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;
    proxy_http_version 1.1;
  }
}
