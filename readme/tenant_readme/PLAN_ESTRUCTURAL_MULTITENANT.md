# 🏗️ **Plan Estructural Multi-tenant con PostgreSQL**
## Sistema Chalan-Pro Optimizado para VPS

---

## 📊 **Arquitectura General Multi-tenant**

```
┌─────────────────────────────────────────────────────────────────┐
│                    VPS SERVER (Ubuntu 22.04)                   │
│                     IP: xxx.xxx.xxx.xxx                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            ┌───────▼───────┐       ┌───────▼───────┐
            │   PRODUCTION  │       │      QA       │
            │ MULTI-TENANT  │       │ MULTI-TENANT  │
            │  ENVIRONMENT  │       │  ENVIRONMENT  │
            └───────────────┘       └───────────────┘
```

---

## 🐳 **Contenedores Docker - Producción Multi-tenant**

### **1. Nginx Proxy (nginx-proxy)**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: nginx-proxy                                      │
│ Image: jwilder/nginx-proxy                                  │
│ Ports: 80, 443                                             │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Archivos:                                                   │
│ ├── /etc/nginx/conf.d/default.conf                         │
│ ├── /etc/nginx/certs/                                      │
│ │   ├── phoenixelectricandair.net.crt                      │
│ │   ├── phoenixelectricandair.net.key                      │
│ │   ├── client2.example.com.crt                           │
│ │   ├── client2.example.com.key                           │
│ │   ├── client3.example.com.crt                           │
│ │   └── client3.example.com.key                           │
│ └── /var/log/nginx/                                        │
└─────────────────────────────────────────────────────────────┘
```

### **2. Let's Encrypt Companion**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: nginx-proxy-letsencrypt-1                       │
│ Image: jrcs/letsencrypt-nginx-proxy-companion              │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Funciones:                                                  │
│ ├── Renovación automática de certificados SSL              │
│ ├── Generación de certificados para nuevos dominios        │
│ ├── Soporte multi-tenant con múltiples dominios            │
│ └── Monitoreo de expiración                                │
└─────────────────────────────────────────────────────────────┘
```

### **3. Frontend Multi-tenant (Vue.js)**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-phoenix-nginx-1                          │
│ Image: nginx:1.19.0-alpine                                 │
│ Ports: 80 (internal)                                       │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Configuración Tenant:                                       │
│ ├── VIRTUAL_HOST: phoenixelectricandair.net                │
│ ├── LETSENCRYPT_HOST: phoenixelectricandair.net            │
│ ├── TENANT_SCHEMA: tenant_phoenix                          │
│ └── TENANT_ID: phoenix_001                                 │
├─────────────────────────────────────────────────────────────┤
│ Volúmenes:                                                  │
│ ├── ./vuefrontend/dist → /usr/share/nginx/html             │
│ └── ./vuefrontend/nginx.conf → /etc/nginx/conf.d/default.conf │
└─────────────────────────────────────────────────────────────┘
```

### **4. Backend Multi-tenant (Django)**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-phoenix-web-1                            │
│ Image: chalanpro:2.0.0                                     │
│ Ports: 8000 (internal)                                     │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Configuración Tenant:                                       │
│ ├── VIRTUAL_HOST: api.phoenixelectricandair.net            │
│ ├── LETSENCRYPT_HOST: api.phoenixelectricandair.net        │
│ ├── TENANT_SCHEMA: tenant_phoenix                          │
│ ├── DATABASE_URL: postgresql://user:pass@db:5432/chalan_tenant_db │
│ └── TENANT_MODE: schema                                     │
├─────────────────────────────────────────────────────────────┤
│ Volúmenes:                                                  │
│ ├── . → /app                                               │
│ └── ./logs → /app/logs                                     │
└─────────────────────────────────────────────────────────────┘
```

### **5. PostgreSQL Multi-tenant**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-phoenix-db-1                             │
│ Image: postgres:15-alpine                                  │
│ Ports: 5432 (internal)                                     │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Configuración:                                              │
│ ├── POSTGRES_DB: chalan_tenant_db                          │
│ ├── POSTGRES_USER: chalan_user                             │
│ └── POSTGRES_PASSWORD: secure_password                     │
├─────────────────────────────────────────────────────────────┤
│ Estructura Multi-tenant:                                    │
│ ├── /var/lib/postgresql/data/                              │
│ │   ├── chalan_tenant_db/                                  │
│ │   │   ├── tenant_phoenix/                                │
│ │   │   │   ├── contracts                                  │
│ │   │   │   ├── inventory                                  │
│ │   │   │   ├── schedule                                   │
│ │   │   │   └── transactions                               │
│ │   │   ├── tenant_client2/                                │
│ │   │   │   ├── contracts                                  │
│ │   │   │   ├── inventory                                  │
│ │   │   │   └── schedule                                   │
│ │   │   ├── tenant_client3/                                │
│ │   │   └── public/                                        │
│ │   │       ├── tenants                                    │
│ │   │       ├── users                                      │
│ │   │       └── tenant_subscriptions                       │
│ │   └── init-tenant-schemas.sql                            │
│ └── /docker-entrypoint-initdb.d/                           │
└─────────────────────────────────────────────────────────────┘
```

### **6. Redis Cache**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-phoenix-redis-1                          │
│ Image: redis:7.4-alpine                                    │
│ Ports: 6379 (internal)                                     │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Funciones Multi-tenant:                                     │
│ ├── Cache de sesiones por tenant                           │
│ ├── Cache de consultas de base de datos                    │
│ ├── Cola de tareas (Celery) por tenant                     │
│ └── Rate limiting por tenant                               │
└─────────────────────────────────────────────────────────────┘
```

### **7. PgAdmin (Gestión DB)**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-phoenix-pgadmin-1                        │
│ Image: dpage/pgadmin4:latest                               │
│ Ports: 5050:80                                             │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Funciones:                                                  │
│ ├── Interfaz web para gestión de PostgreSQL                │
│ ├── Gestión de schemas multi-tenant                        │
│ ├── Backup y restore por tenant                            │
│ └── Monitoreo de consultas                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 **Contenedores Docker - QA Multi-tenant**

### **1. Frontend QA Multi-tenant**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-stage-nginx-qa-1                         │
│ Image: nginx:1.19.0-alpine                                 │
│ Ports: 80 (internal)                                       │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Configuración QA:                                           │
│ ├── VIRTUAL_HOST: stage.phoenixelectricandair.net          │
│ ├── LETSENCRYPT_HOST: stage.phoenixelectricandair.net      │
│ ├── TENANT_SCHEMA: tenant_phoenix_qa                       │
│ └── ENVIRONMENT: qa                                        │
└─────────────────────────────────────────────────────────────┘
```

### **2. Backend QA Multi-tenant**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-stage-web-qa-1                           │
│ Image: chalanpro:2.0.0-qa                                  │
│ Ports: 8000 (internal)                                     │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Configuración QA:                                           │
│ ├── VIRTUAL_HOST: api-stage.phoenixelectricandair.net      │
│ ├── LETSENCRYPT_HOST: api-stage.phoenixelectricandair.net  │
│ ├── TENANT_SCHEMA: tenant_phoenix_qa                       │
│ ├── DATABASE_URL: postgresql://user:pass@db-qa:5432/chalan_qa_db │
│ └── ENVIRONMENT: qa                                        │
└─────────────────────────────────────────────────────────────┘
```

### **3. PostgreSQL QA Multi-tenant**
```
┌─────────────────────────────────────────────────────────────┐
│ Container: chalan-stage-db-qa-1                            │
│ Image: postgres:15-alpine                                  │
│ Ports: 5433:5432                                           │
│ Networks: nginx-proxy                                       │
├─────────────────────────────────────────────────────────────┤
│ Configuración QA:                                           │
│ ├── POSTGRES_DB: chalan_qa_db                              │
│ ├── POSTGRES_USER: chalan_qa_user                          │
│ └── Datos de prueba por tenant                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌐 **Configuración de Redes Multi-tenant**

```
┌─────────────────────────────────────────────────────────────┐
│ Network: nginx-proxy                                        │
│ Driver: bridge                                              │
│ Subnet: 172.18.0.0/16                                      │
├─────────────────────────────────────────────────────────────┤
│ Contenedores Multi-tenant:                                  │
│ ├── nginx-proxy (172.18.0.2)                              │
│ ├── nginx-proxy-letsencrypt-1 (172.18.0.3)                │
│ ├── chalan-phoenix-nginx-1 (172.18.0.8)                   │
│ ├── chalan-phoenix-web-1 (172.18.0.9)                     │
│ ├── chalan-client2-nginx-1 (172.18.0.10)                  │
│ ├── chalan-client2-web-1 (172.18.0.11)                    │
│ ├── chalan-client3-nginx-1 (172.18.0.12)                  │
│ ├── chalan-client3-web-1 (172.18.0.13)                    │
│ ├── chalan-phoenix-db-1 (172.18.0.4)                      │
│ ├── chalan-phoenix-redis-1 (172.18.0.5)                   │
│ ├── chalan-phoenix-pgadmin-1 (172.18.0.6)                 │
│ ├── chalan-phoenix-worker-1 (172.18.0.7)                  │
│ ├── chalan-stage-nginx-qa-1 (172.18.0.14)                 │
│ ├── chalan-stage-web-qa-1 (172.18.0.15)                   │
│ └── chalan-stage-db-qa-1 (172.18.0.16)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 **Estructura de Archivos Multi-tenant**

```
/home/superadmin/chalan_pro-phoenix/
├── docker-compose.yml                    # Producción Multi-tenant
├── docker-compose.qa.yml                # QA Multi-tenant
├── docker-compose.local.yml             # Desarrollo local
├── Dockerfile                           # Imagen del backend
├── requirements.txt                     # Dependencias Python
├── manage.py                           # Django management
├── .env                                # Variables de entorno
├── .env.qa                             # Variables QA
├── .env_mysql                          # Configuración PostgreSQL
├── project/                            # Configuración Django
│   ├── settings/                       # Settings por ambiente
│   │   ├── __init__.py
│   │   ├── base.py                     # Configuración base
│   │   ├── production.py               # Producción
│   │   ├── qa.py                       # QA
│   │   └── local.py                    # Local
│   ├── urls.py
│   └── wsgi.py
├── appcore/                            # Apps compartidas
│   ├── models.py                       # Modelos tenant
│   ├── views.py
│   └── admin.py
├── vuefrontend/                        # Frontend Vue.js
│   ├── package.json
│   ├── vue.config.js
│   ├── nginx.conf
│   ├── dist/                           # Build de producción
│   └── src/                            # Código fuente
│       ├── components/
│       ├── views/
│       ├── store/                      # Vuex/Pinia
│       └── router/                     # Router con tenant
├── appinventory/                       # Apps por tenant
├── appschedule/
├── apptransactions/
├── ctrctsapp/
├── crewsapp/
├── docker/                             # Scripts Docker
│   ├── postgres/
│   │   ├── init-multiple-databases.sh
│   │   ├── init-tenant-schemas.sql
│   │   └── create-tenant.sh
│   └── nginx/
│       └── tenant-config.conf
├── scripts/                            # Scripts de gestión
│   ├── create-tenant.sh
│   ├── backup-tenant.sh
│   ├── migrate-tenant.sh
│   └── deploy.sh
├── logs/                               # Logs por tenant
│   ├── phoenix/
│   ├── client2/
│   └── client3/
├── media/                              # Archivos multimedia
│   ├── phoenix/
│   ├── client2/
│   └── client3/
└── staticfiles/                        # Archivos estáticos
    ├── phoenix/
    ├── client2/
    └── client3/
```

---

## 🔧 **Docker Compose Multi-tenant**

### **docker-compose.yml**
```yaml
version: '3.8'

services:
  # PostgreSQL Multi-tenant
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=chalan_tenant_db
      - POSTGRES_USER=chalan_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_MULTIPLE_DATABASES=chalan_tenant_db
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./docker/postgres/init-multiple-databases.sh:/docker-entrypoint-initdb.d/
      - ./docker/postgres/init-tenant-schemas.sql:/docker-entrypoint-initdb.d/
    ports:
      - "5432:5432"
    networks:
      - nginx-proxy

  # Redis Cache
  redis:
    image: redis:7.4-alpine
    volumes:
      - redis-data:/data
    networks:
      - nginx-proxy

  # Backend Phoenix Tenant
  web-phoenix:
    image: chalanpro:2.0.0
    build:
      context: .
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    environment:
      - VIRTUAL_HOST=api.phoenixelectricandair.net
      - LETSENCRYPT_HOST=api.phoenixelectricandair.net
      - TENANT_SCHEMA=tenant_phoenix
      - TENANT_ID=phoenix_001
      - DATABASE_URL=postgresql://chalan_user:${DB_PASSWORD}@db:5432/chalan_tenant_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - .:/app
      - ./logs/phoenix:/app/logs
    networks:
      - nginx-proxy
    depends_on:
      - db
      - redis

  # Frontend Phoenix Tenant
  nginx-phoenix:
    image: nginx:1.19.0-alpine
    volumes:
      - ./vuefrontend/dist:/usr/share/nginx/html
      - ./vuefrontend/nginx.conf:/etc/nginx/conf.d/default.conf
    environment:
      - VIRTUAL_HOST=phoenixelectricandair.net,www.phoenixelectricandair.net
      - LETSENCRYPT_HOST=phoenixelectricandair.net,www.phoenixelectricandair.net
      - TENANT_SCHEMA=tenant_phoenix
    networks:
      - nginx-proxy
    depends_on:
      - web-phoenix

  # Backend Client2 Tenant
  web-client2:
    image: chalanpro:2.0.0
    command: python manage.py runserver 0.0.0.0:8000
    environment:
      - VIRTUAL_HOST=api.client2.example.com
      - LETSENCRYPT_HOST=api.client2.example.com
      - TENANT_SCHEMA=tenant_client2
      - TENANT_ID=client2_001
      - DATABASE_URL=postgresql://chalan_user:${DB_PASSWORD}@db:5432/chalan_tenant_db
      - REDIS_URL=redis://redis:6379/1
    volumes:
      - .:/app
      - ./logs/client2:/app/logs
    networks:
      - nginx-proxy
    depends_on:
      - db
      - redis

  # Frontend Client2 Tenant
  nginx-client2:
    image: nginx:1.19.0-alpine
    volumes:
      - ./vuefrontend/dist:/usr/share/nginx/html
      - ./vuefrontend/nginx.conf:/etc/nginx/conf.d/default.conf
    environment:
      - VIRTUAL_HOST=client2.example.com,www.client2.example.com
      - LETSENCRYPT_HOST=client2.example.com,www.client2.example.com
      - TENANT_SCHEMA=tenant_client2
    networks:
      - nginx-proxy
    depends_on:
      - web-client2

  # PgAdmin
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@phoenixelectricandair.net
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD}
      - PGADMIN_CONFIG_SERVER_MODE=False
    ports:
      - "5050:80"
    networks:
      - nginx-proxy
    depends_on:
      - db

  # Worker para tareas asíncronas
  worker:
    image: chalanpro:2.0.0
    command: celery -A project worker -l info
    environment:
      - DATABASE_URL=postgresql://chalan_user:${DB_PASSWORD}@db:5432/chalan_tenant_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - .:/app
    networks:
      - nginx-proxy
    depends_on:
      - db
      - redis

volumes:
  postgres-data:
  redis-data:

networks:
  nginx-proxy:
    external: true
```

---

## 🗄️ **Estructura de Base de Datos Multi-tenant**

### **Esquemas por Tenant**
```sql
-- Base de datos: chalan_tenant_db

-- Schema público (compartido)
public.tenants                    -- Información de tenants
public.users                      -- Usuarios globales
public.tenant_subscriptions       -- Suscripciones
public.tenant_settings           -- Configuraciones globales

-- Schema Phoenix Electric
tenant_phoenix.contracts         -- Contratos Phoenix
tenant_phoenix.inventory         -- Inventario Phoenix
tenant_phoenix.schedule          -- Programación Phoenix
tenant_phoenix.transactions      -- Transacciones Phoenix
tenant_phoenix.crews             -- Cuadrillas Phoenix

-- Schema Client2
tenant_client2.contracts         -- Contratos Client2
tenant_client2.inventory         -- Inventario Client2
tenant_client2.schedule          -- Programación Client2
tenant_client2.transactions      -- Transacciones Client2

-- Schema Client3
tenant_client3.contracts         -- Contratos Client3
tenant_client3.inventory         -- Inventario Client3
tenant_client3.schedule          -- Programación Client3
tenant_client3.transactions      -- Transacciones Client3
```

---

## 🚀 **Flujo de Tráfico Multi-tenant**

```
Internet → VPS (80/443) → nginx-proxy → {
    ├── phoenixelectricandair.net → nginx-phoenix → web-phoenix → tenant_phoenix schema
    ├── www.phoenixelectricandair.net → nginx-phoenix → web-phoenix → tenant_phoenix schema
    ├── api.phoenixelectricandair.net → web-phoenix → tenant_phoenix schema
    ├── client2.example.com → nginx-client2 → web-client2 → tenant_client2 schema
    ├── www.client2.example.com → nginx-client2 → web-client2 → tenant_client2 schema
    ├── api.client2.example.com → web-client2 → tenant_client2 schema
    ├── client3.example.com → nginx-client3 → web-client3 → tenant_client3 schema
    └── api.client3.example.com → web-client3 → tenant_client3 schema
}
```

---

## 📊 **Recursos y Optimizaciones Multi-tenant**

### **Recursos Asignados:**
- **VPS**: 8GB RAM, 4 CPU cores, 160GB SSD
- **Producción**: 70% de recursos
- **QA**: 30% de recursos
- **Por Tenant**: ~2GB RAM, 1 CPU core

### **Optimizaciones Multi-tenant:**
- **SSL/TLS**: Certificados automáticos por dominio
- **Cache**: Redis con separación por tenant (DB 0, 1, 2...)
- **Compresión**: Gzip en Nginx
- **CDN**: Para archivos estáticos por tenant
- **Backup**: Automático por schema de tenant
- **Monitoreo**: Logs separados por tenant
- **Rate Limiting**: Por tenant
- **Isolation**: Schemas separados en PostgreSQL

---

## 🔧 **Scripts de Gestión Multi-tenant**

### **create-tenant.sh**
```bash
#!/bin/bash
# Crear nuevo tenant

TENANT_NAME=$1
SCHEMA_NAME=$2
DOMAIN=$3
TENANT_ID=$4

echo "Creando tenant: $TENANT_NAME"

# Crear schema en PostgreSQL
docker exec chalan-phoenix-db-1 psql -U chalan_user -d chalan_tenant_db -c "
CREATE SCHEMA IF NOT EXISTS ${SCHEMA_NAME};
INSERT INTO public.tenants (name, schema_name, domain, tenant_id) 
VALUES ('${TENANT_NAME}', '${SCHEMA_NAME}', '${DOMAIN}', '${TENANT_ID}');
"

# Crear contenedores para el nuevo tenant
docker run -d \
  --name chalan-${SCHEMA_NAME}-web \
  --network nginx-proxy \
  -e VIRTUAL_HOST=${DOMAIN},www.${DOMAIN} \
  -e LETSENCRYPT_HOST=${DOMAIN},www.${DOMAIN} \
  -e TENANT_SCHEMA=${SCHEMA_NAME} \
  -e TENANT_ID=${TENANT_ID} \
  chalanpro:2.0.0

docker run -d \
  --name chalan-${SCHEMA_NAME}-nginx \
  --network nginx-proxy \
  -e VIRTUAL_HOST=${DOMAIN},www.${DOMAIN} \
  -e LETSENCRYPT_HOST=${DOMAIN},www.${DOMAIN} \
  -e TENANT_SCHEMA=${SCHEMA_NAME} \
  nginx:1.19.0-alpine

echo "Tenant ${TENANT_NAME} creado exitosamente"
```

### **backup-tenant.sh**
```bash
#!/bin/bash
# Backup específico por tenant

TENANT_SCHEMA=$1
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)

echo "Creando backup para tenant: $TENANT_SCHEMA"

# Crear directorio de backup
mkdir -p ./backups/${TENANT_SCHEMA}

# Backup del schema específico
docker exec chalan-phoenix-db-1 pg_dump \
  -U chalan_user \
  -d chalan_tenant_db \
  -n ${TENANT_SCHEMA} \
  > ./backups/${TENANT_SCHEMA}/${TENANT_SCHEMA}_${BACKUP_DATE}.sql

echo "Backup creado: ./backups/${TENANT_SCHEMA}/${TENANT_SCHEMA}_${BACKUP_DATE}.sql"
```

---

## 📈 **Ventajas del Sistema Multi-tenant**

1. **Aislamiento de datos**: Cada tenant tiene su propio schema
2. **Escalabilidad**: Fácil agregar nuevos clientes
3. **Mantenimiento**: Una sola aplicación para múltiples clientes
4. **Costo-efectivo**: Compartir recursos de infraestructura
5. **Personalización**: Cada tenant puede tener configuraciones específicas
6. **Seguridad**: Datos completamente separados
7. **Backup granular**: Backup por tenant individual
8. **Monitoreo específico**: Logs y métricas por tenant

---

## 🚀 **Plan de Migración Multi-tenant**

### **Fase 1: Preparación**
- [X] Migrar de MySQL a PostgreSQL
- [ ] Implementar django-tenant-schemas
- [ ] Configurar esquemas base

### **Fase 2: Desarrollo**
- [ ] Crear modelos multi-tenant
- [ ] Implementar middleware de tenant
- [ ] Configurar routing por dominio

### **Fase 3: Testing**
- [ ] Crear entorno QA multi-tenant
- [ ] Testing de aislamiento de datos
- [ ] Testing de rendimiento

### **Fase 4: Producción**
- [ ] Migrar datos existentes
- [ ] Configurar dominios de producción
- [ ] Monitoreo y alertas

### **Fase 5: Optimización**
- [ ] Optimización de consultas
- [ ] Cache por tenant
- [ ] Backup automatizado

---

**Este plan estructural proporciona un sistema multi-tenant robusto, escalable y mantenible con PostgreSQL, permitiendo múltiples clientes en una sola infraestructura con aislamiento completo de datos.**

---

*Documento generado para sistema Chalan-Pro Multi-tenant*  
*Fecha: $(date)*  
*Versión: 2.0.0*
