# 🚀 Crear Ambiente Multi-Tenant en Render.com

## 📋 Situación Actual

- ✅ **Servicios existentes:**
  - `chalan-backend` (Web Service) - Rama: `main`
  - `chalan-frontend` (Static Site) - Rama: `main`
  - `chalan-db` (PostgreSQL) - Plan: Free

- ✅ **Nueva rama creada:** `tenantDB` en `chalan_pro_render`

## 🎯 Opciones para Configurar el Ambiente Multi-Tenant

### Opción 1: Actualizar Servicio Existente (Recomendada)

Actualizar el servicio `chalan-backend` para usar la rama `tenantDB`:

**Ventajas:**
- Usa recursos existentes
- No requiere crear nuevos servicios
- Más económico

**Pasos:**
1. En Render Dashboard → `chalan-backend` → Settings
2. Cambiar **Branch** de `main` a `tenantDB`
3. Agregar variables de entorno necesarias para multi-tenant
4. Guardar y desplegar

**Variables de entorno a agregar:**
```bash
# Multi-tenant Configuration
DJANGO_TENANTS=True
SHARED_APPS=tenants,public
TENANT_APPS=appinventory,apptransactions,appschedule,appcore,crewsapp,ctrctsapp,auditapp
DATABASE_ROUTERS=tenant_schemas.routers.TenantSyncRouter
PUBLIC_SCHEMA_URLCONF=project.urls_public
TENANT_MODEL=tenants.Tenant
```

### Opción 2: Crear Nuevo Servicio Web (Aislamiento Total)

Crear un nuevo servicio web específico para multi-tenant:

**Ventajas:**
- Ambiente completamente aislado
- Puede usar diferentes configuraciones
- Permite probar sin afectar producción

**Desventajas:**
- Requiere plan de pago adicional (si excedes el free tier)
- Más recursos consumidos

## 🔧 Configuración Recomendada (Opción 1)

### Paso 1: Actualizar Variables de Entorno

Agregar estas variables al servicio `chalan-backend`:

```bash
# Django Core (ya existentes)
DJANGO_SETTINGS_MODULE=project.settings
SECRET_KEY=<tu-secret-key>
ALLOWED_HOSTS=*
DEBUG=False

# Database (ya configurada)
DATABASE_URL=<de chalan-db>

# Multi-Tenant Configuration (NUEVAS)
DJANGO_TENANTS=True
SHARED_APPS=tenants,public
TENANT_APPS=appinventory,apptransactions,appschedule,appcore,crewsapp,ctrctsapp,auditapp
DATABASE_ROUTERS=tenant_schemas.routers.TenantSyncRouter
PUBLIC_SCHEMA_URLCONF=project.urls_public
TENANT_MODEL=tenants.Tenant

# Onboarding
ENABLE_ONBOARDING=True
ONBOARDING_DOMAIN=chalan-pro.net

# CORS y Seguridad
CSRF_TRUSTED_ORIGINS=https://chalan-backend.onrender.com,https://*.chalan-pro.net
CORS_ALLOWED_ORIGINS=https://chalan-frontend.onrender.com,https://*.chalan-pro.net
```

### Paso 2: Actualizar Build Command

El build command debe incluir migraciones para schemas:

```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate_schemas --shared
```

### Paso 3: Actualizar Start Command

```bash
daphne -b 0.0.0.0 -p $PORT project.asgi:application
```

### Paso 4: Cambiar Branch a `tenantDB`

En Render Dashboard:
1. Ve a `chalan-backend` → Settings
2. En **Build & Deploy**, cambia **Branch** a `tenantDB`
3. Guarda cambios
4. Render desplegará automáticamente

## 📊 Base de Datos Multi-Tenant

### Estructura Esperada

La base de datos `chalan-db` tendrá:
- **Schema público (`public`):** Tablas compartidas (tenants, domains)
- **Schemas de tenant:** Un schema por cada tenant (ej: `tenant_globo_dyned2`)

### Migraciones Iniciales

Después del primer despliegue, ejecuta:

```bash
# Migrar schema público (shared apps)
python manage.py migrate_schemas --shared

# Crear schemas para tenants existentes (si los hay)
python manage.py migrate_schemas
```

## 🔍 Verificación Post-Despliegue

1. **Verificar que el servicio está corriendo:**
   ```bash
   curl https://chalan-backend.onrender.com/admin/
   ```

2. **Verificar endpoint de onboarding:**
   ```bash
   curl https://chalan-backend.onrender.com/api/onboarding/create-tenant/
   ```

3. **Verificar creación de tenant:**
   - Acceder a `/onboarding` desde el frontend
   - Completar el formulario
   - Verificar que se crea el schema en la base de datos

## 🚨 Notas Importantes

1. **Base de datos:** Render solo permite 1 base de datos gratuita. El sistema multi-tenant usa la misma base de datos pero con múltiples schemas.

2. **Dominios:** Para que los subdominios funcionen en producción, necesitarás:
   - Configurar DNS wildcard (`*.chalan-pro.net` → IP de Render)
   - O usar un dominio personalizado en Render

3. **Migraciones:** Las migraciones se ejecutan automáticamente en el build, pero para schemas específicos de tenant, pueden necesitarse comandos adicionales.

4. **Logs:** Revisa los logs de Render si hay errores durante el despliegue:
   - Dashboard → `chalan-backend` → Logs

## 📝 Próximos Pasos

1. ✅ Configurar MCP en Cursor (ver `CONFIGURAR_MCP_CURSOR.md`)
2. ⏳ Actualizar servicio en Render para usar rama `tenantDB`
3. ⏳ Agregar variables de entorno multi-tenant
4. ⏳ Verificar despliegue y funcionalidad
5. ⏳ Probar creación de tenant vía onboarding

