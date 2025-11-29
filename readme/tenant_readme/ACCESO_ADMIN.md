# 🔐 Acceso al Admin - Credenciales

## ✅ Superusuarios Creados

### 1. Admin Global (Schema Public)

**URLs de Acceso**:
- http://localhost:8000/admin/
- http://192.168.0.248:8000/admin/

**Credenciales**:
- **Usuario**: `admin`
- **Email**: `admin@chalan-pro.net`
- **Contraseña**: `admin123`

**Funcionalidad**:
- ✅ Gestionar tenants (crear, editar, eliminar)
- ✅ Gestionar dominios de tenants
- ✅ Configuración global del sistema
- ✅ Ver todos los tenants registrados

---

### 2. Admin del Tenant Phoenix

**URL de Acceso**:
- http://phoenix.chalan-pro.net:8000/admin/
- **Nota**: Requiere configurar `/etc/hosts` para desarrollo local

**Credenciales**:
- **Usuario**: `phoenix_admin`
- **Email**: `phoenix@chalan-pro.net`
- **Contraseña**: `phoenix123`

**Funcionalidad**:
- ✅ Gestionar datos del tenant Phoenix Electric
- ✅ Acceso a todas las apps:
  - Inventory (Productos, Categorías, Almacenes)
  - Transactions (Documentos, Partes, Tipos)
  - Schedule (Eventos, Calendario)
  - Contracts (Contratos, Constructores, Trabajos)
  - Crews (Cuadrillas, Camiones)
  - Audit (Logs de acciones)
- ✅ Datos completamente aislados del schema public y otros tenants

---

## 🔧 Configurar /etc/hosts (Desarrollo Local)

Para acceder al admin del tenant desde desarrollo local, necesitas configurar el archivo hosts:

### Windows

Editar: `C:\Windows\System32\drivers\etc\hosts`

Agregar:
```
127.0.0.1    phoenix.chalan-pro.net
127.0.0.1    client2.chalan-pro.net
```

**Nota**: Puede requerir permisos de administrador para editar.

### Linux/Mac

Editar: `/etc/hosts`

Agregar:
```
127.0.0.1    phoenix.chalan-pro.net
127.0.0.1    client2.chalan-pro.net
```

---

## 🔒 Cambiar Contraseñas

### Cambiar Contraseña del Admin Global

```bash
docker exec chalan-backend python manage.py changepassword admin
```

### Cambiar Contraseña del Admin del Tenant

```bash
docker exec chalan-backend python manage.py changepassword phoenix_admin --schema=phoenix
```

O usando Python:

```bash
docker exec chalan-backend python manage.py shell
```

```python
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

User = get_user_model()

with schema_context('phoenix'):
    user = User.objects.get(username='phoenix_admin')
    user.set_password('nueva_contraseña_segura')
    user.save()
    print('Contraseña actualizada')
```

---

## 🆕 Crear Nuevos Superusuarios

### Para Schema Public (Admin Global)

```bash
docker exec chalan-backend python manage.py createsuperuser
```

### Para un Tenant Específico

```bash
docker exec chalan-backend python manage.py create_tenant_superuser \
    -s phoenix \
    --username nuevo_usuario \
    --email usuario@ejemplo.com \
    --noinput
```

Luego establecer la contraseña:

```bash
docker exec chalan-backend python manage.py changepassword nuevo_usuario --schema=phoenix
```

---

## ⚠️ Seguridad en Producción

**IMPORTANTE**: Estas credenciales son solo para desarrollo. En producción:

1. ✅ Cambia todas las contraseñas por contraseñas seguras y únicas
2. ✅ Usa variables de entorno para credenciales sensibles
3. ✅ Considera implementar autenticación de dos factores (2FA)
4. ✅ Limita el acceso al admin solo desde IPs autorizadas
5. ✅ Usa HTTPS con certificados SSL válidos
6. ✅ Implementa rate limiting para prevenir ataques de fuerza bruta

---

## 📊 Verificación de Usuarios

### Ver Usuarios en Schema Public

```bash
docker exec chalan-backend python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); [print(f'{u.username} - {u.email}') for u in User.objects.all()]"
```

### Ver Usuarios en Schema Phoenix

```bash
docker exec chalan-backend python manage.py shell -c "from django_tenants.utils import schema_context; from django.contrib.auth import get_user_model; User = get_user_model(); exec('with schema_context(\"phoenix\"): [print(f\"{u.username} - {u.email}\") for u in User.objects.all()]')"
```

---

**Última actualización**: 2025-11-24  
**Versión**: 1.0.0

