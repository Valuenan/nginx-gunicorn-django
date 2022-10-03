# Запуск задания

## Базовые настройки

Устанавливем библиотеки

```dash
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

Заходим в интерактивную сессию postgres

```dash
sudo -u postgres psql
```

Создаем базу

```dash
CREATE DATABASE test;
```

Создаем пользователя базы

```dash
CREATE USER admin WITH PASSWORD 'admin';
```

Даем доступ пользователю к базе

```dash
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

Выходим из интеративного режима

```dash
/q
```

Подтягиваем зависимости

```dash
pip install -r requirements.txt
```

Создать исключение для порта 8000

```dash
sudo ufw allow 8000
```

## Настрока gunicorn

Создаем и открываем systemd socket

```dash
sudo nano /etc/systemd/system/gunicorn.socket
```

прописываем настроки

```dash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Настройка systemd service

```dash
sudo nano /etc/systemd/system/gunicorn.service
```
прописываем настроки

```dash
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=osboxes
Group=www-data
WorkingDirectory=/home/osboxes/PycharmProjects/pythonProject/project
ExecStart=/home/osboxes/PycharmProjects/pythonProject/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Запускаем и делаем что бы система автоматически устанавливала соединение с gunicorn.service, при подключении к сокету

```dash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

#Проверка

Проверяем что gunicorn.sock существует

```dash
file /run/gunicorn.sock
```

Проверяем что механизм активации сокета работает и смотрим статус

```dash
curl --unix-socket /run/gunicorn.sock localhost
sudo systemctl status gunicorn
```

## Настройка nginx

Создаем папки для статики и передаем права пользователю

```dash
sudo mkdir -pv /var/www/127.0.0.1/static/
sudo chown -cR osboxes /var/www/127.0.0.1/
```

Копируем статику

```dash
sudo python3 manage.py collectstatic
```

Переводим дебаг в False

Настройка файла sites-available

```dash
sudo nano /etc/nginx/sites-available/project
```
прописываем настройки

```dash 
server {
    listen 85;
    server_name localhost;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /var/www/127.0.0.1/static/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Включаем наш файл добавляя в sites-enabled

```dash
sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled
```

Тестируем конфиг

```dash
sudo nginx -t
```

Открываем доступ на 85 порт

```dash
sudo ufw allow 'Nginx Full'
```

Рестарт gunicorn, nginx

```dash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```
