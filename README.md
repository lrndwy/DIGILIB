# Digilib (Diginusa Library)

## Frontend Environment
```
VITE_VPV_LICENSE=8ac115b7-b578-4a6b-af83-84c687aa2daf
VITE_API_URL=http://localhost:8000
```

## Backend Environment
```
# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Django
DJANGO_SECRET_KEY=django-insecure-+juae91n+ca7c7m+ha2_94ef30l=i9s%6v_ik&b1n!zhh7@=oh
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=7

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
ACCESS_CONTROL_ALLOW_ORIGIN=http://localhost:5173,http://localhost:3000
```

## Watermark 
go to this folder and run this command
```bash
sudo cp watermark.webp ./frontend/node_modules/@vue-pdf-viewer/viewer/dist/assets/
```

Vue 3 + Django.
By lrndwy


