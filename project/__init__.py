"""
Inicialización temprana del proyecto.
Este archivo se ejecuta antes de que Django cargue settings.py,
permitiendo aplicar patches necesarios para desarrollo.
"""
import os

# Aplicar monkey patch para permitir hostnames con guiones bajos en desarrollo
# Esto debe hacerse MUY TEMPRANO, antes de que Django valide cualquier hostname
if os.environ.get('DEBUG', 'False') == 'True':
    try:
        # Intentar aplicar el patch tan temprano como sea posible
        import django
        # Solo aplicar si Django está disponible
        if hasattr(django, 'http'):
            import django.http.request
            
            # Guardar la función original
            if hasattr(django.http.request, 'validate_host'):
                _original_validate_host_django = django.http.request.validate_host
            else:
                _original_validate_host_django = None
            
            def _relaxed_validate_host_early(host, allowed_hosts):
                """
                Validación relajada de hostnames para desarrollo.
                Permite guiones bajos en hostnames locales.
                """
                # Remover puerto si existe
                host_without_port = host.split(':')[0] if ':' in host else host
                
                # Si el hostname contiene guiones bajos, usar validación relajada
                if '_' in host_without_port:
                    # Verificar si está en allowed_hosts (exacto o con wildcard)
                    if host_without_port in allowed_hosts:
                        return True
                    # Verificar wildcards (ej: .chalan-pro.net)
                    for allowed_host in allowed_hosts:
                        if allowed_host.startswith('.') and host_without_port.endswith(allowed_host):
                            return True
                    # Permitir hostnames con guiones bajos en desarrollo
                    return True
                
                # Para hostnames sin guiones bajos, usar validación estándar
                if _original_validate_host_django:
                    return _original_validate_host_django(host, allowed_hosts)
                # Fallback: validación básica
                return host_without_port in allowed_hosts or any(
                    allowed_host.startswith('.') and host_without_port.endswith(allowed_host)
                    for allowed_host in allowed_hosts
                )
            
            # Aplicar el patch
            django.http.request.validate_host = _relaxed_validate_host_early
    except Exception:
        # Si hay error, continuar sin el patch (se aplicará en settings.py)
        pass

