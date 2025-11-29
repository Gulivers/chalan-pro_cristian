# 🔧 Solución: Error 404 "No tenant for hostname localhost"

## Problema

Al acceder a `http://localhost:8000/admin/` se obtenía el error:

```
Page not found (404)
No tenant for hostname "localhost"
```

## Causa

django-tenants requiere que cada dominio tenga un tenant asociado. Cuando se accede a `localhost`, el middleware busca un tenant con ese dominio, pero no existía.

## Solución Implementada

### 1. Crear Tenant para Schema Public

Se creó un tenant especial con `schema_name='public'` y un dominio `localhost` asociado:

```python
from tenants.models import Tenant, Domain
from django_tenants.utils import get_public_schema_name

public_schema = get_public_schema_name()  # Retorna 'public'

# Crear tenant para schema public
tenant, created = Tenant.objects.get_or_create(
    schema_name=public_schema,
    defaults={
        'name': 'Public Schema',
        'is_active': True
    }
)

# Crear dominio localhost asociado
domain, d_created = Domain.objects.get_or_create(
    domain='localhost',
    defaults={
        'tenant': tenant,
        'is_primary': True
    }
)
```

### 2. Configuración en settings.py

Se agregó la configuración para permitir acceso al schema public:

```python
# Configuración para desarrollo local
# Permitir acceso al schema public si no se encuentra tenant
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
PUBLIC_SCHEMA_URLCONF = 'project.urls_public'
```

## Verificación

### Verificar Dominios Configurados

```bash
docker exec chalan-backend python manage.py shell -c "from tenants.models import Domain; domains = Domain.objects.all(); [print(f'{d.domain} -> {d.tenant.name} ({d.tenant.schema_name})') for d in domains]"
```

Debería mostrar:
```
phoenix.chalan-pro.net -> Phoenix Electric (phoenix)
localhost -> Public Schema (public)
```

### Acceso al Sistema

Ahora puedes acceder a:

1. **Admin Global** (schema public):
   - URL: http://localhost:8000/admin/
   - Gestiona tenants y configuración global

2. **Admin del Tenant Phoenix**:
   - URL: http://phoenix.chalan-pro.net:8000/admin/
   - Requiere configurar /etc/hosts para desarrollo local

## Comandos Útiles

### Crear Dominio para Schema Public

```bash
docker exec chalan-backend python manage.py shell -c "
from tenants.models import Tenant, Domain
from django_tenants.utils import get_public_schema_name

public_schema = get_public_schema_name()
tenant, _ = Tenant.objects.get_or_create(
    schema_name=public_schema,
    defaults={'name': 'Public Schema', 'is_active': True}
)
domain, created = Domain.objects.get_or_create(
    domain='localhost',
    defaults={'tenant': tenant, 'is_primary': True}
)
print(f'Domain created: {created}')
"
```

### Agregar Otros Dominios para Desarrollo

Para agregar `127.0.0.1`:

```bash
docker exec chalan-backend python manage.py shell -c "
from tenants.models import Tenant, Domain
from django_tenants.utils import get_public_schema_name

public_schema = get_public_schema_name()
tenant = Tenant.objects.get(schema_name=public_schema)
Domain.objects.get_or_create(
    domain='127.0.0.1',
    defaults={'tenant': tenant, 'is_primary': False}
)
print('Domain 127.0.0.1 added')
"
```

## Notas Importantes

1. **Schema Public**: El schema `public` es especial en django-tenants. Contiene los modelos compartidos (Tenant, Domain).

2. **Dominios Múltiples**: Un tenant puede tener múltiples dominios. El dominio marcado como `is_primary=True` es el principal.

3. **Desarrollo vs Producción**: 
   - En desarrollo: usar `localhost` o `127.0.0.1`
   - En producción: usar dominios reales como `admin.chalan-pro.net`

4. **Reiniciar Backend**: Después de crear dominios, puede ser necesario reiniciar el contenedor:
   ```bash
   docker restart chalan-backend
   ```

## Estado Actual

✅ **Problema Resuelto**

- Tenant "Public Schema" creado con schema_name='public'
- Dominio 'localhost' asociado al schema public
- Configuración SHOW_PUBLIC_IF_NO_TENANT_FOUND activada
- Backend reiniciado para aplicar cambios

Ahora puedes acceder a http://localhost:8000/admin/ sin problemas.

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0

