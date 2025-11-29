# 🏗️ Implementación Multi-tenant con django-tenants

## 📋 Resumen

Este documento describe la implementación del sistema multi-tenant usando **django-tenants** con PostgreSQL y el modelo **Single Database, Multiple Schemas**.

## 🎯 Arquitectura

### Conceptos Clave

- **Single Database**: Una sola base de datos PostgreSQL (`chalan_sch_per_tenant`)
- **Multiple Schemas**: Cada tenant tiene su propio schema (ej: `phoenix`, `client2`)
- **Schema Public**: Contiene la tabla `tenants` y `domains` para gestionar todos los tenants
- **Subdomain Routing**: El sistema identifica el tenant mediante el subdominio (ej: `phoenix.chalan-pro.net`)

### Flujo de Petición

```
1. Usuario accede a: https://phoenix.chalan-pro.net
           ↓
2. NGINX recibe la petición y pasa al backend Django
           ↓
3. Middleware django-tenants detecta el subdominio "phoenix"
           ↓
4. Busca el tenant con dominio "phoenix.chalan-pro.net"
           ↓
5. Cambia el search_path de PostgreSQL al schema "phoenix"
           ↓
6. Django procesa la petición usando solo datos del schema "phoenix"
           ↓
7. Respuesta con datos aislados del tenant
```

## 📦 Instalación y Configuración

### 1. Dependencias

El paquete `django-tenants` ya está incluido en `requirements.txt`:

```txt
django-tenants>=3.5.0
psycopg2-binary>=2.9.9
```

### 2. Estructura de Apps

Las apps están divididas en dos categorías:

#### SHARED_APPS (Schema 'public')
- `django_tenants`
- `tenants` (modelo Tenant)
- `django.contrib.contenttypes`
- `django.contrib.auth`
- `django.contrib.admin`
- `project` (configuración)

#### TENANT_APPS (Cada schema de tenant)
- `auditapp`
- `ctrctsapp`
- `crewsapp`
- `appschedule`
- `appinventory`
- `apptransactions`
- `appcore`

### 3. Configuración de Base de Datos

En `project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # IMPORTANTE
        'NAME': 'chalan_sch_per_tenant',
        'USER': 'postgres',
        'PASSWORD': 'chalan2024',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"
DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)
```

### 4. Middleware

El middleware de django-tenants **DEBE** ir primero:

```python
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # PRIMERO
    # ... resto de middlewares
]
```

## 🗄️ Estructura de Base de Datos

### Schema 'public' (Compartido)

```sql
public.tenants_tenant          -- Información de todos los tenants
public.tenants_domain          -- Dominios asociados a cada tenant
public.django_migrations       -- Migraciones compartidas
public.auth_user               -- Usuarios globales (opcional)
```

### Schema por Tenant (ej: 'phoenix')

```sql
phoenix.ctrctsapp_contract     -- Contratos del tenant
phoenix.appinventory_product   -- Productos del tenant
phoenix.appschedule_event      -- Eventos del tenant
phoenix.apptransactions_*      -- Transacciones del tenant
phoenix.django_migrations      -- Migraciones del tenant
phoenix.auth_user              -- Usuarios del tenant
```

## 🚀 Uso

### Crear un Nuevo Tenant

#### Opción 1: Desde el Admin Django

1. Acceder al admin global: `http://localhost:8000/admin/` (o dominio público)
2. Ir a **Tenants** → **Add Tenant**
3. Completar:
   - **Name**: Nombre del cliente (ej: "Phoenix Electric")
   - **Schema name**: Nombre del schema (ej: "phoenix")
   - **Domain**: Dominio completo (ej: "phoenix.chalan-pro.net")
   - **Is active**: Activar el tenant
4. Guardar

#### Opción 2: Comando de Gestión

```bash
python manage.py create_tenant \
    --name "Phoenix Electric" \
    --schema phoenix \
    --domain phoenix.chalan-pro.net \
    --trial
```

### Migraciones

#### Migraciones para Schema 'public'

```bash
python manage.py migrate_schemas --schema=public
```

#### Migraciones para un Tenant Específico

```bash
python manage.py migrate_schemas --schema=phoenix
```

#### Migraciones para Todos los Tenants

```bash
python manage.py migrate_schemas
```

### Acceder al Admin de un Tenant

- **Admin Global** (schema public): `http://localhost:8000/admin/`
- **Admin del Tenant**: `http://phoenix.chalan-pro.net/admin/`

## 🔧 Configuración de Desarrollo Local

### 1. Configurar /etc/hosts (Windows)

Editar `C:\Windows\System32\drivers\etc\hosts`:

```
127.0.0.1    phoenix.chalan-pro.net
127.0.0.1    client2.chalan-pro.net
```

### 2. Configurar Docker Compose

El archivo `docker-compose.yml` ya está configurado con:
- Base de datos: `chalan_sch_per_tenant`
- Puerto PostgreSQL: `5432`
- Puerto Backend: `8000`

### 3. Inicializar la Base de Datos

```bash
# Crear migraciones para el schema public
python manage.py makemigrations
python manage.py migrate_schemas --schema=public

# Crear el primer tenant
python manage.py create_tenant \
    --name "Phoenix Electric" \
    --schema phoenix \
    --domain phoenix.chalan-pro.net

# Ejecutar migraciones para el tenant
python manage.py migrate_schemas --schema=phoenix
```

## 🌐 Configuración de Producción (Render.com)

### Variables de Entorno

```env
DATABASE_URL=postgresql://user:pass@host:5432/chalan_sch_per_tenant
ALLOWED_HOSTS=*.chalan-pro.net,*.onrender.com,chalan-backend.onrender.com
```

### NGINX Configuration

Para producción, necesitarás configurar NGINX para pasar el header `Host` al backend:

```nginx
server {
    listen 80;
    server_name *.chalan-pro.net;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 📝 Comandos Útiles

### Listar Todos los Tenants

```python
from tenants.models import Tenant
tenants = Tenant.objects.all()
for tenant in tenants:
    print(f"{tenant.name} - {tenant.schema_name}")
```

### Acceder a Datos de un Tenant Específico

```python
from django_tenants.utils import schema_context

with schema_context('phoenix'):
    # Todas las consultas aquí usan el schema 'phoenix'
    contracts = Contract.objects.all()
```

### Crear Usuario en un Tenant

```python
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

User = get_user_model()

with schema_context('phoenix'):
    user = User.objects.create_user(
        username='admin',
        email='admin@phoenix.com',
        password='password123'
    )
```

## 🔒 Seguridad

### Aislamiento de Datos

- Cada tenant tiene su propio schema
- Las consultas SQL automáticamente usan el `search_path` correcto
- No hay forma de acceder a datos de otro tenant sin cambiar explícitamente el schema

### Validación de Dominios

- django-tenants valida que el dominio existe antes de procesar la petición
- Si el dominio no existe, retorna 404

## 🐛 Troubleshooting

### Error: "relation does not exist"

**Causa**: Las migraciones no se han ejecutado para el tenant.

**Solución**:
```bash
python manage.py migrate_schemas --schema=<schema_name>
```

### Error: "schema does not exist"

**Causa**: El tenant no se creó correctamente o el schema no existe.

**Solución**:
1. Verificar que el tenant existe: `Tenant.objects.filter(schema_name='phoenix').exists()`
2. Crear el schema manualmente si es necesario

### Error: "Invalid schema name"

**Causa**: El nombre del schema no es válido para PostgreSQL.

**Solución**: 
- Usar solo letras, números y guiones bajos
- No empezar con número
- Máximo 63 caracteres

## 📚 Referencias

- [django-tenants Documentation](https://django-tenants.readthedocs.io/)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)

## ✅ Checklist de Implementación

- [x] Instalar django-tenants
- [x] Crear app `tenants` con modelo Tenant
- [x] Configurar SHARED_APPS y TENANT_APPS
- [x] Configurar DATABASES con django_tenants.postgresql_backend
- [x] Agregar TenantMainMiddleware
- [x] Crear admin global para gestionar tenants
- [x] Crear comando create_tenant
- [x] Actualizar docker-compose.yml
- [x] Documentación completa

---

**Última actualización**: 2025-11-24  
**Versión**: 1.0.0

