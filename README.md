
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
./.venv/Scripts/Activate.bat
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