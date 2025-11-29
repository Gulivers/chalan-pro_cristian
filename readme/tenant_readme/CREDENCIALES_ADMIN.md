# 🔐 Credenciales de Acceso al Admin

## 👤 Superusuarios Creados

### Admin Global (Schema Public)

**URL**: http://localhost:8000/admin/

**Credenciales**:
- **Usuario**: `admin`
- **Email**: `admin@chalan-pro.net`
- **Contraseña**: `admin123`

**Funcionalidad**:
- Gestionar tenants (crear, editar, eliminar)
- Gestionar dominios de tenants
- Configuración global del sistema

---

### Admin del Tenant Phoenix

**URL**: http://phoenix.chalan-pro.net:8000/admin/  
(Requiere configurar /etc/hosts para desarrollo local)

**Credenciales**:
- **Usuario**: `phoenix_admin`
- **Email**: `phoenix@chalan-pro.net`
- **Contraseña**: `phoenix123`

**Funcionalidad**:
- Gestionar datos del tenant Phoenix Electric
- Acceso a todas las apps: inventory, transactions, schedule, contracts, etc.
- Datos completamente aislados del schema public y otros tenants

---

## 🔒 Seguridad

⚠️ **IMPORTANTE**: Estas son credenciales de desarrollo. En producción:

1. Cambia todas las contraseñas por contraseñas seguras
2. Usa variables de entorno para credenciales sensibles
3. Considera usar autenticación de dos factores (2FA)
4. Limita el acceso al admin solo desde IPs autorizadas

## 📝 Cambiar Contraseñas

### Cambiar Contraseña del Admin Global

```bash
docker exec chalan-backend python manage.py changepassword admin
```

### Cambiar Contraseña del Admin del Tenant

```bash
docker exec chalan-backend python manage.py shell -c "
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model
User = get_user_model()
with schema_context('phoenix'):
    user = User.objects.get(username='phoenix_admin')
    user.set_password('nueva_contraseña_segura')
    user.save()
    print('Contraseña actualizada')
"
```

## 🆕 Crear Nuevos Superusuarios

### Para Schema Public

```bash
docker exec chalan-backend python manage.py createsuperuser
```

### Para un Tenant Específico

```bash
docker exec chalan-backend python manage.py shell
```

```python
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

User = get_user_model()

with schema_context('phoenix'):  # Cambiar 'phoenix' por el schema deseado
    User.objects.create_superuser(
        username='nuevo_usuario',
        email='usuario@ejemplo.com',
        password='contraseña_segura'
    )
```

---

**Última actualización**: 2025-11-24  
**Versión**: 1.0.0

