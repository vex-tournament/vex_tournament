# vex_tournament

A website to manage robotics tournaments, built using Django. The production website is accessible at https://vex.thearchons.xyz/.

# Getting Started
## Requirements
- Python 3
- Django
- Gunicorn (production only)
- Just (production only)

## Installation
1. Clone the repository
2. Run `pip install -r requirements.txt` to install the packages
3. Add a `.env` file to the project root (where `manage.py` is)

The `.env` stores settings that are used by `vex_tournament/settings.py`. Here is an example:
```json
{
    "debug": true,
    "key": "YOUR-SECRET-KEY-HERE",
    "allowed_hosts": ["127.0.0.1"],
    "static_root": ""
}
```

- `debug` is for use when debugging. This should be set to false when running in production for security reasons.
- `key` is a secret key used by django. Generate one [here](https://djecrety.ir).
- `allowed_hosts` are the allowed hosts/domains. For development servers, the default is `127.0.0.1`
- `static_root` is where your static files will be collected when running `python manage.py collectstatic`. This can be left blank for development.

4. Run `python manage.py makemigrations` and then `python manage.py migrate` to setup the database.
5. Create a superuser with `python manage.py createsuperuser`.
6. Run the server with `python manage.py runserver`

If you only need it for development. The site should now be accessible at `127.0.0.1`. However, more configuration is required to run a secure production server.

7. Collect static files with `python manage.py collectstatic`.
8. Because `python manage.py runserver` is for development servers and is insecure, you should run the server with gunicorn instead. Run `gunicorn vex_tournament.wsgi:application --bind 0.0.0.0:8000` to start the server.
9. The server should now be accessible at `0.0.0.0:8000`, but will not include CSS for the admin site. In order to make it accessible from the internet, use a reverse proxy such as [nginx](https://nginx.org).
10. In order to enable the CSS, set the `/static` location to your static root location. Here is an example nginx configuration that is similar to the one used by the production server.
```nginx
access_log                  /var/log/nginx/vex.access.log;
error_log                   /var/log/nginx/vex.error.log;

server {
  server_name               vex.thearchons.xyz;
  listen                    80;
  return                    307 https://$host$request_uri;
}

server {
  server_name               vex.thearchons.xyz;
  listen 443 ssl;
  #ssl on;
  ssl_certificate /var/www/cert.pem;
  ssl_certificate_key /var/www/key.pem;

  location / {
      proxy_pass              http://127.0.1.1:8000;
      proxy_set_header        Host $host;
  }

  location /static {
       autoindex on;
       alias /home/archons/vex_tournament/static_root;
  }
}
```
12. The production server uses the `justfile` to start the server. Configure the justfile and run `just` in the project directory to easily start the server.

## Usage
The main site will not be useful until the tournament is configured. Configure the server at `YOUR-URL/admin`. To reset the playoffs, delete every object in `Playoff Matches` and `Brackets` at `YOUR-URL/admin`.
