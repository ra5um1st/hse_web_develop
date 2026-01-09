
# Запуск

## Docker Compose

Только БД:
```powershell
docker compose --profile db up -d
```

## Windows

```powershell
python -m venv .venv
```
```powershell
./.venv/Scripts/activate
```
```powershell
pip install -r requirements.txt
```
```powershell
install-gdal
```
```powershell
python ./src/manage.py runserver 127.0.0.1:8080
```

# Migrations

```powershell
python ./src/manage.py makemigrations
```
```powershell
python ./src/manage.py migrate
```
```powershell
$env:DJANGO_SUPERUSER_USERNAME="admin"
$env:DJANGO_SUPERUSER_EMAIL="admin@example.com"
$env:DJANGO_SUPERUSER_PASSWORD="admin"

python ./src/manage.py createsuperuser --no-input
```
```powershell
python ./src/manage.py loaddata ./dumpdata/auth_user.json ./dumpdata/events.json ./dumpdata/tags.json ./dumpdata/event_tags.json
```