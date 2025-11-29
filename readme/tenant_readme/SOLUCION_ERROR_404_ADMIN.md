# 🔧 Solución: Error 404 al acceder al Admin del Tenant

## Problema

Al acceder a `http://globo_dyned2.chalan-pro.net:8000/admin/` se obtiene un error 404:

```
Not Found: /admin/
HTTP GET /admin/ 404
```

## Causas Posibles

### 1. El hostname incluye el puerto

Cuando accedes a `http://globo_dyned2.chalan-pro.net:8000/admin/`, Django recibe el hostname como `globo_dyned2.chalan-pro.net:8000` (con el puerto), pero el dominio en la base de datos es solo `globo_dyned2.chalan-pro.net` (sin puerto).

**Solución**: django-tenants debería manejar esto automáticamente, pero si no funciona, verifica que el dominio esté correctamente configurado.

### 2. El dominio no está en ALLOWED_HOSTS

Aunque django-tenants maneja los subdominios, Django primero verifica `ALLOWED_HOSTS`.

**Solución**: Asegúrate de que el dominio esté en `ALLOWED_HOSTS` o usa el formato `.chalan-pro.net` (con punto inicial).

### 3. Las migraciones no se aplicaron al schema del tenant

Si las migraciones del admin no se aplicaron al schema del tenant, el admin no estará disponible.

**Solución**: Ejecuta las migraciones para el schema específico:

```bash
docker exec -it chalan-backend python manage.py migrate_schemas --schema=globo_dyned2
```

## Soluciones

### Solución 1: Verificar y corregir el dominio

```bash
docker exec -it chalan-backend python manage.py shell
```

```python
from tenants.models import Domain, Tenant

# Verificar el dominio
domain = Domain.objects.filter(domain__icontains='globo_dyned2').first()
print(f"Domain: {domain.domain}")
print(f"Tenant: {domain.tenant.name}")
print(f"Schema: {domain.tenant.schema_name}")

# Si el dominio no existe o está mal, crear/corregir
tenant = Tenant.objects.get(schema_name='globo_dyned2')
domain, created = Domain.objects.get_or_create(
    domain='globo_dyned2.chalan-pro.net',
    defaults={
        'tenant': tenant,
        'is_primary': True
    }
)
print(f"Domain {'creado' if created else 'actualizado'}: {domain.domain}")
```

### Solución 2: Aplicar migraciones al schema

```bash
# Aplicar todas las migraciones al schema del tenant
docker exec -it chalan-backend python manage.py migrate_schemas --schema=globo_dyned2

# Verificar que las tablas del admin existan
docker exec -it chalan-backend python manage.py shell
```

```python
from django_tenants.utils import schema_context
from tenants.models import Tenant
from django.db import connection

tenant = Tenant.objects.get(schema_name='globo_dyned2')
with schema_context(tenant.schema_name):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'globo_dyned2' 
        AND table_name LIKE 'django_%'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    print("Tablas Django en schema globo_dyned2:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Verificar específicamente las tablas del admin
    admin_tables = ['django_admin_log', 'django_content_type', 'auth_user', 'auth_group']
    for table in admin_tables:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'globo_dyned2' 
                AND table_name = '{table}'
            )
        """)
        exists = cursor.fetchone()[0]
        print(f"{table}: {'✓' if exists else '✗'}")
```

### Solución 3: Verificar que django-tenants detecte el tenant

```bash
docker exec -it chalan-backend python manage.py shell
```

```python
from django_tenants.utils import get_tenant_model
from django_tenants.utils import tenant_context

Tenant = get_tenant_model()

# Simular la detección del tenant
hostname = 'globo_dyned2.chalan-pro.net'
# Remover el puerto si existe
hostname = hostname.split(':')[0]

try:
    domain = Domain.objects.select_related('tenant').get(domain=hostname)
    tenant = domain.tenant
    print(f"✓ Tenant detectado: {tenant.name}")
    print(f"  Schema: {tenant.schema_name}")
    print(f"  Domain: {domain.domain}")
    print(f"  Is Active: {tenant.is_active}")
    
    # Verificar que el schema existe
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.schemata 
            WHERE schema_name = '{tenant.schema_name}'
        )
    """)
    schema_exists = cursor.fetchone()[0]
    print(f"  Schema existe: {'✓' if schema_exists else '✗'}")
    
except Domain.DoesNotExist:
    print(f"✗ No se encontró dominio para: {hostname}")
```

### Solución 4: Acceder sin puerto (usando proxy)

Si estás usando un proxy o nginx, configura el proxy para que no incluya el puerto en el hostname:

```nginx
proxy_set_header Host $host;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Proto $scheme;
```

## Verificación Final

Después de aplicar las soluciones, verifica:

1. **El dominio existe**:
   ```bash
   docker exec -it chalan-backend python manage.py list_tenants
   ```

2. **Las migraciones están aplicadas**:
   ```bash
   docker exec -it chalan-backend python manage.py migrate_schemas --schema=globo_dyned2 --list
   ```

3. **El admin está accesible**:
   - Abre: `http://globo_dyned2.chalan-pro.net:8000/admin/`
   - Deberías ver la página de login del admin

4. **Verificar logs del backend**:
   ```bash
   docker logs chalan-backend --tail 50 | grep -i "admin\|tenant\|404"
   ```

## Notas Importantes

1. **Puerto en desarrollo**: En desarrollo local, Django puede recibir el puerto en el hostname. django-tenants debería manejar esto, pero si no funciona, considera usar un proxy que elimine el puerto.

2. **ALLOWED_HOSTS**: Asegúrate de que el dominio esté en `ALLOWED_HOSTS` o usa el formato `.chalan-pro.net` (con punto inicial) para permitir todos los subdominios.

3. **Cache del navegador**: Limpia la caché del navegador después de hacer cambios.

---

**Fecha**: 2025-11-25  
**Versión**: 1.0.0

