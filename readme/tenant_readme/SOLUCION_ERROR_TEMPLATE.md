# 🔧 Solución: Error NoReverseMatch en Template Admin

## Problema

Al acceder al admin desde `localhost` o `192.168.0.248:8000`, se obtenía el error:

```
NoReverseMatch at /admin/login/
Reverse for 'inventory-dashboard' not found. 'inventory-dashboard' is not a valid view function or pattern name.
```

## Causa

El template `appinventory/templates/admin/base_site.html` estaba intentando hacer un reverse a la URL `'inventory-dashboard'`, pero esta URL solo existe en los schemas de tenant, no en el schema `public`.

Cuando accedes al admin desde `localhost` (schema public), las apps de tenant (como `appinventory`) no están disponibles porque están en `TENANT_APPS`, no en `SHARED_APPS`.

## Solución Implementada

Se modificó el template para que solo muestre el enlace al dashboard cuando estamos en un tenant (no en el schema public):

```django
{% extends "admin/base_site.html" %}

{% block branding %}
  <h1 id="site-name">
    <a href="{% url 'admin:index' %}">Chalan Admin</a>
  </h1>
  {% comment %} Solo mostrar el enlace al dashboard si estamos en un tenant (no en schema public) {% endcomment %}
  {% if request.tenant and request.tenant.schema_name != 'public' %}
  <div style="margin-top: 10px;">
    <a href="/dashboard/" class="button default" style="margin-top:5px;">
      📊 Go to Dashboard
    </a>
  </div>
  {% endif %}
{% endblock %}
```

### Cambios Realizados

1. **Verificación de Tenant**: Se agregó la condición `{% if request.tenant and request.tenant.schema_name != 'public' %}` para verificar que estamos en un tenant antes de mostrar el enlace.

2. **URL Directa**: En lugar de usar `{% url 'inventory-dashboard' %}`, se usa la URL directa `/dashboard/` para evitar el error de reverse cuando la URL no está disponible.

3. **Condicional**: El bloque completo del enlace solo se muestra cuando estamos en un tenant, no en el schema public.

## Verificación

### Acceso al Admin Global (Schema Public)

- URL: http://localhost:8000/admin/
- Comportamiento: El enlace al dashboard **NO** se muestra
- Razón: Estamos en el schema public, donde las apps de tenant no están disponibles

### Acceso al Admin del Tenant (Schema Phoenix)

- URL: http://phoenix.chalan-pro.net:8000/admin/
- Comportamiento: El enlace al dashboard **SÍ** se muestra
- Razón: Estamos en el schema phoenix, donde las apps de tenant están disponibles

## Notas Importantes

1. **Templates de Tenant**: Los templates en `appinventory/templates/admin/` solo deberían usarse cuando estamos en un tenant, pero Django puede encontrarlos también en el schema public.

2. **Verificación de Tenant**: Siempre verificar `request.tenant` y su `schema_name` antes de acceder a URLs o funcionalidades específicas de tenant.

3. **URLs Directas vs Reverse**: En algunos casos, usar URLs directas puede ser más seguro que usar `{% url %}` cuando no estás seguro de que la URL exista en el contexto actual.

## Archivos Modificados

- `appinventory/templates/admin/base_site.html` - Template corregido para verificar el tenant antes de mostrar el enlace

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0

