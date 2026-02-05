server {
  listen 80 http;
  server_name sandbox.com;

  root /var/www/html/;
  index index.html index.htm;

  client_max_body_size 100M;

  location /browser/ {
    proxy_pass http://127.0.0.1:8081/;
    proxy_buffering off;
    proxy_redirect off;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
