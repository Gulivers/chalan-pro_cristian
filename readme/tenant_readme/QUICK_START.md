# 🚀 Quick Start - Multi-tenant Setup

## Pasos Rápidos para Configurar el Sistema Multi-tenant

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` basado en `env.example`:

```env
POSTGRES_DB=chalan_sch_per_tenant
POSTGRES_USER=postgres
POSTGRES_PASSWORD=chalan2024
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*.chalan-pro.net
```

### 3. Iniciar Contenedores Docker

```bash
docker-compose up -d
```

### 4. Crear Migraciones para Schema Public

```bash
docker exec -it chalan-backend python manage.py makemigrations
docker exec -it chalan-backend python manage.py migrate_schemas --schema=public
```

### 5. Crear Superusuario para Admin Global

```bash
docker exec -it chalan-backend python manage.py createsuperuser
```

### 6. Crear Primer Tenant

```bash
docker exec -it chalan-backend python manage.py create_tenant \
    --name "Phoenix Electric" \
    --schema phoenix \
    --domain phoenix.chalan-pro.net
```

### 7. Ejecutar Migraciones para el Tenant

```bash
docker exec -it chalan-backend python manage.py migrate_schemas --schema=phoenix
```

### 8. Configurar /etc/hosts (Desarrollo Local)

**Windows**: Editar `C:\Windows\System32\drivers\etc\hosts`

```
127.0.0.1    phoenix.chalan-pro.net
127.0.0.1    client2.chalan-pro.net
```

**Linux/Mac**: Editar `/etc/hosts`

```
127.0.0.1    phoenix.chalan-pro.net
127.0.0.1    client2.chalan-pro.net
```

### 9. Acceder al Sistema

- **Admin Global**: http://localhost:8000/admin/
- **Admin Tenant**: http://phoenix.chalan-pro.net:8000/admin/
- **API Tenant**: http://phoenix.chalan-pro.net:8000/api/

## ✅ Verificación

### Verificar que el Tenant se Creó

```bash
docker exec -it chalan-backend python manage.py shell
```

```python
from tenants.models import Tenant
tenants = Tenant.objects.all()
for t in tenants:
    print(f"{t.name} - {t.schema_name}")
```

### Verificar Schemas en PostgreSQL

```bash
docker exec -it chalan_postgres psql -U postgres -d chalan_sch_per_tenant -c "\dn"
```

Deberías ver:
- `public` (schema compartido)
- `phoenix` (schema del tenant)

## 🎯 Próximos Pasos

1. Crear más tenants según necesidad
2. Configurar NGINX para producción
3. Configurar certificados SSL con Let's Encrypt
4. Revisar la documentación completa en `IMPLEMENTACION_DJANGO_TENANTS.md`

