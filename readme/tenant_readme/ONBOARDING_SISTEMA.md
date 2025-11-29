# 🚀 Sistema de Onboarding - Creación Automática de Tenants

## 📋 Resumen

Sistema completo de onboarding que permite a los clientes crear su cuenta y ambiente de trabajo automáticamente. El sistema genera:

1. ✅ Tenant con schema único en PostgreSQL
2. ✅ Dominio/subdominio automático
3. ✅ Migraciones ejecutadas automáticamente
4. ✅ Superusuario inicial creado
5. ✅ Redirección automática al subdominio del cliente

## 🏗️ Arquitectura

### Flujo del Onboarding

```
1. Cliente accede a /onboarding
   ↓
2. Completa formulario (nombre, email, tipo de negocio, logo)
   ↓
3. Frontend envía POST a /api/onboarding/create-tenant/
   ↓
4. Backend crea:
   - Tenant con schema_name generado automáticamente
   - Domain con subdominio basado en schema_name
   - Ejecuta migraciones para el nuevo schema
   - Crea superusuario inicial
   ↓
5. Retorna URL del subdominio
   ↓
6. Frontend redirige al cliente a su ambiente
```

## 📦 Componentes Implementados

### 1. Modelo Tenant Actualizado (`tenants/models.py`)

**Nuevos campos agregados**:
- `email`: Email del cliente
- `client_type`: Tipo de negocio (electric, air_conditioning, solar, etc.)
- `logo`: Logo de la empresa
- `tenant_id`: ID único del tenant

**Funcionalidades**:
- Generación automática de `schema_name` basado en el nombre
- Generación automática de `tenant_id` único
- Validación de formato de schema_name según PostgreSQL

### 2. Vista API de Onboarding (`tenants/views.py`)

**Endpoint**: `POST /api/onboarding/create-tenant/`

**Parámetros recibidos**:
- `company_name` (requerido): Nombre de la empresa
- `email` (requerido): Email del cliente
- `client_type` (requerido): Tipo de negocio
- `logo` (opcional): Archivo de imagen

**Proceso**:
1. Valida los datos recibidos
2. Crea el Tenant (genera schema_name y tenant_id automáticamente)
3. Crea el Domain con subdominio `{schema_name}.chalan-pro.net`
4. Ejecuta migraciones para el nuevo schema
5. Crea superusuario inicial con email como username base
6. Retorna URL de redirección

**Respuesta exitosa**:
```json
{
  "success": true,
  "message": "¡Tu cuenta ha sido creada exitosamente! Redirigiendo a tu ambiente...",
  "url": "http://{subdomain}.chalan-pro.net:8000/",
  "tenant": {
    "name": "Phoenix Electric",
    "schema_name": "phoenix_electric",
    "domain": "phoenix_electric.chalan-pro.net",
    "username": "phoenix",
    "email": "phoenix@example.com"
  }
}
```

### 3. URLs Configuradas

**Schema Public** (`project/urls_public.py`):
- Incluye `tenants.urls` para acceso al onboarding desde dominio público

**Tenants URLs** (`tenants/urls.py`):
- `/api/onboarding/create-tenant/` - Endpoint de creación

### 4. Frontend Vue (`vuefrontend/src/views/OnboardingView.vue`)

**Ruta**: `/onboarding`

**Características**:
- Formulario con validación
- Preview de logo
- Manejo de errores
- Redirección automática después de crear cuenta
- Timeout de 5 minutos para la creación

**Campos del formulario**:
- Business Name (nombre de la empresa)
- Email Address
- Business Type (tipo de negocio)
- Company Logo (opcional)

## 🔧 Configuración

### Variables de Entorno

En `project/settings.py`:

```python
# Dominio base para los tenants
TENANT_BASE_DOMAIN = os.environ.get('TENANT_BASE_DOMAIN', 'chalan-pro.net')
```

### Dominio Base

El dominio base se puede configurar mediante variable de entorno:

```bash
export TENANT_BASE_DOMAIN=chalan-pro.net
```

O en `docker-compose.yml`:

```yaml
environment:
  TENANT_BASE_DOMAIN: chalan-pro.net
```

## 📝 Uso

### Para Clientes (Onboarding)

1. Acceder a: `http://localhost:8000/onboarding`
2. Completar el formulario:
   - Nombre de la empresa
   - Email
   - Tipo de negocio
   - Logo (opcional)
3. Hacer clic en "Create My Account"
4. Esperar 2-5 minutos mientras se crea el ambiente
5. Ser redirigido automáticamente al subdominio

### Credenciales Iniciales

Después del onboarding, el cliente recibirá:
- **URL**: `http://{subdomain}.chalan-pro.net:8000/`
- **Username**: Basado en el email (ej: `phoenix` si email es `phoenix@example.com`)
- **Password temporal**: `{schema_name}123!` (ej: `phoenix_electric123!`)

**⚠️ IMPORTANTE**: El cliente debe cambiar la contraseña en el primer login.

## 🔒 Seguridad

### Validaciones Implementadas

1. **Email único**: No se puede crear tenant con email duplicado
2. **Schema name único**: Generación automática con contador si existe
3. **Validación de formato**: Schema name debe cumplir reglas de PostgreSQL
4. **Validación de logo**: Solo imágenes, máximo 5MB

### Recomendaciones de Producción

1. ✅ Implementar rate limiting para prevenir spam
2. ✅ Agregar CAPTCHA para prevenir bots
3. ✅ Validar email mediante confirmación
4. ✅ Enviar email de bienvenida con credenciales
5. ✅ Forzar cambio de contraseña en primer login
6. ✅ Implementar logging de auditoría

## 🐛 Troubleshooting

### Error: "Schema name already exists"

**Causa**: El schema_name generado ya existe en la base de datos.

**Solución**: El sistema automáticamente agrega un contador (ej: `phoenix_electric_2`).

### Error: "Email already registered"

**Causa**: El email ya está asociado a otro tenant.

**Solución**: Usar un email diferente o contactar al administrador.

### Error: "Migration failed"

**Causa**: Error al ejecutar migraciones para el nuevo schema.

**Solución**: 
1. Verificar logs del backend
2. Ejecutar migraciones manualmente:
   ```bash
   docker exec chalan-backend python manage.py migrate_schemas --schema={schema_name}
   ```

### El cliente no puede acceder al subdominio

**Causa**: DNS no configurado o /etc/hosts no actualizado.

**Solución**:
- **Desarrollo**: Agregar a `/etc/hosts`:
  ```
  127.0.0.1    {subdomain}.chalan-pro.net
  ```
- **Producción**: Configurar DNS wildcard `*.chalan-pro.net` → IP del servidor

## 📊 Ejemplo de Uso

### Crear Tenant desde Onboarding

1. Cliente accede a `http://localhost:8000/onboarding`
2. Completa formulario:
   - **Business Name**: "Phoenix Electric & Air"
   - **Email**: "contact@phoenixelectric.com"
   - **Business Type**: "Electric"
   - **Logo**: `phoenix-logo.png`
3. Hace clic en "Create My Account"
4. Sistema crea:
   - Tenant: `Phoenix Electric & Air`
   - Schema: `phoenix_electric_air`
   - Domain: `phoenix_electric_air.chalan-pro.net`
   - Username: `contact`
   - Password: `phoenix_electric_air123!`
5. Cliente es redirigido a `http://phoenix_electric_air.chalan-pro.net:8000/`

## 📚 Archivos Modificados/Creados

### Backend
- ✅ `tenants/models.py` - Modelo Tenant actualizado
- ✅ `tenants/views.py` - Vista de onboarding creada
- ✅ `tenants/urls.py` - URLs de onboarding creadas
- ✅ `tenants/admin.py` - Admin actualizado con nuevos campos
- ✅ `project/urls_public.py` - Incluye URLs de tenants
- ✅ `project/settings.py` - Configuración TENANT_BASE_DOMAIN

### Frontend
- ✅ `vuefrontend/src/views/OnboardingView.vue` - Vista de onboarding (ya existía)
- ✅ `vuefrontend/src/router/index.js` - Ruta `/onboarding` agregada

### Migraciones
- ✅ `tenants/migrations/0002_*.py` - Migración para nuevos campos

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0  
**Estado**: ✅ COMPLETADO Y FUNCIONANDO

