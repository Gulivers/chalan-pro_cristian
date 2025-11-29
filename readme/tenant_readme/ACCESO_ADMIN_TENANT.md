# 🔐 Acceso al Admin de Cada Tenant

## 📋 Resumen

Este documento explica cómo acceder al admin de Django para cada tenant creado usando su subdominio personalizado.

## 🎯 Acceso por Subdominio

Cada tenant tiene su propio subdominio que permite acceder a su ambiente aislado. Por ejemplo:
- **Tenant**: Globo Dyned2
- **Schema**: `globo_dyned2`
- **Dominio**: `globo_dyned2.chalan-pro.net`
- **URL Admin**: `http://globo_dyned2.chalan-pro.net:8000/admin/`

## 🖥️ Configuración para Desarrollo Local (Windows)

### Paso 1: Configurar el archivo hosts

En Windows, necesitas editar el archivo `hosts` para que el subdominio apunte a `localhost`:

1. **Abrir el Bloc de notas como Administrador**:
   - Presiona `Win + X`
   - Selecciona "Windows PowerShell (Administrador)" o "Símbolo del sistema (Administrador)"
   - O busca "Notepad" en el menú inicio, clic derecho → "Ejecutar como administrador"

2. **Abrir el archivo hosts**:
   - En el Bloc de notas, ve a: `Archivo → Abrir`
   - Navega a: `C:\Windows\System32\drivers\etc\`
   - Cambia el filtro de "Documentos de texto" a "Todos los archivos"
   - Abre el archivo `hosts` (sin extensión)

3. **Agregar las entradas para cada tenant**:
   ```
   127.0.0.1    globo_dyned2.chalan-pro.net
   127.0.0.1    phoenix.chalan-pro.net
   127.0.0.1    localhost
   ```

4. **Guardar el archivo** (Ctrl + S)

### Paso 2: Verificar que el dominio existe en la base de datos

Puedes verificar los dominios creados ejecutando este comando en Django shell:

```bash
docker exec -it chalan-backend python manage.py shell
```

Luego en el shell:
```python
from tenants.models import Domain, Tenant

# Ver todos los dominios
domains = Domain.objects.all()
for domain in domains:
    print(f"Tenant: {domain.tenant.name}")
    print(f"Domain: {domain.domain}")
    print(f"Schema: {domain.tenant.schema_name}")
    print(f"Is Primary: {domain.is_primary}")
    print("---")
```

### Paso 3: Acceder al admin del tenant

Una vez configurado el archivo hosts, puedes acceder al admin de cada tenant:

**URLs de ejemplo:**
- `http://globo_dyned2.chalan-pro.net:8000/admin/`
- `http://phoenix.chalan-pro.net:8000/admin/`

**Credenciales:**
- Las credenciales del superusuario se crean automáticamente durante el onboarding
- En desarrollo, la contraseña temporal se incluye en la respuesta JSON del endpoint `/api/onboarding/`
- Usuario: generalmente el email del administrador (sin el @dominio.com)
- Contraseña: generada automáticamente (en desarrollo se muestra en la respuesta)

## 🔍 Verificar Credenciales del Tenant

### Opción 1: Desde la respuesta del onboarding

Si creaste el tenant desde el frontend, la respuesta incluye las credenciales:

```json
{
  "success": true,
  "tenant": {
    "username": "oliver",
    "email": "oliver.usa1017@gmail.com"
  },
  "credentials": {
    "username": "oliver",
    "password": "abc123XYZ!@#"
  }
}
```

### Opción 2: Consultar directamente en la base de datos

```sql
-- Conectarte al schema del tenant
SET search_path TO globo_dyned2;

-- Ver usuarios del tenant
SELECT username, email, is_staff, is_superuser 
FROM auth_user 
WHERE is_superuser = true;
```

### Opción 3: Crear/Resetear contraseña desde Django shell

```bash
docker exec -it chalan-backend python manage.py shell
```

```python
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model
from tenants.models import Tenant

User = get_user_model()

# Obtener el tenant
tenant = Tenant.objects.get(schema_name='globo_dyned2')

# Cambiar al contexto del tenant
with schema_context(tenant.schema_name):
    # Obtener el superusuario
    user = User.objects.filter(is_superuser=True).first()
    
    if user:
        # Cambiar la contraseña
        user.set_password('nueva_contraseña123')
        user.save()
        print(f"Contraseña cambiada para usuario: {user.username}")
    else:
        print("No se encontró superusuario")
```

## 🌐 Acceso en Producción

En producción (con DNS configurado), simplemente accede a:

```
https://globo_dyned2.chalan-pro.net/admin/
```

No necesitas configurar el archivo hosts porque el DNS ya resuelve el subdominio.

## 🔧 Troubleshooting

### Error: "This site can't be reached"

**Causa**: El archivo hosts no está configurado correctamente o el navegador tiene caché DNS.

**Solución**:
1. Verifica que el archivo hosts tenga la entrada correcta
2. Reinicia el navegador
3. Limpia la caché DNS de Windows:
   ```cmd
   ipconfig /flushdns
   ```

### Error: "Invalid HTTP_HOST header"

**Causa**: El dominio no está en `ALLOWED_HOSTS`.

**Solución**: Verifica que `ALLOWED_HOSTS` en `settings.py` incluya:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.chalan-pro.net',  # Wildcard para todos los subdominios
    'globo_dyned2.chalan-pro.net',  # Específico
    'phoenix.chalan-pro.net',  # Específico
]
```

### Error: "No tenant found"

**Causa**: El dominio no existe en la tabla `tenants_domain`.

**Solución**: Verifica que el dominio esté creado:
```python
from tenants.models import Domain
Domain.objects.filter(domain='globo_dyned2.chalan-pro.net').exists()
```

### El admin muestra datos de otro tenant

**Causa**: El middleware de django-tenants no está detectando correctamente el tenant.

**Solución**: 
1. Verifica que `TenantMainMiddleware` esté primero en `MIDDLEWARE`
2. Verifica que el dominio en la base de datos coincida exactamente con la URL
3. Limpia la caché del navegador

## 📝 Notas Importantes

1. **Cada tenant tiene su propio admin**: Los datos están completamente aislados por schema
2. **Usuarios separados**: Cada tenant tiene su propia tabla `auth_user` en su schema
3. **Migraciones independientes**: Cada tenant puede tener diferentes versiones de migraciones
4. **Dominio público**: Para acceder al admin global (schema `public`), usa `http://localhost:8000/admin/` sin subdominio

## 🚀 Ejemplo Completo

```bash
# 1. Verificar que el backend esté corriendo
docker ps | grep chalan-backend

# 2. Verificar dominios creados
docker exec -it chalan-backend python manage.py shell
>>> from tenants.models import Domain
>>> Domain.objects.all().values('domain', 'tenant__name', 'tenant__schema_name')

# 3. Configurar hosts (Windows)
# Editar C:\Windows\System32\drivers\etc\hosts
# Agregar: 127.0.0.1 globo_dyned2.chalan-pro.net

# 4. Acceder al admin
# http://globo_dyned2.chalan-pro.net:8000/admin/
```

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0

