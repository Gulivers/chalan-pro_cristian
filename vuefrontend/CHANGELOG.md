# Chalan-Pro Frontend – CHANGELOG.md

## Semana de ajustes: Última semana de marzo 2025
Entorno QA: stage.division16llc.net  
Ubicación del proyecto: vuefrontend/

---

### 1. Limpieza y reestructuración de importaciones
- Se eliminó el archivo index.js en components/contracts/ para evitar errores de importación circular.
- Se reemplazaron importaciones indirectas por importaciones directas desde archivos individuales.
- Se mantuvo el uso de alias (@) únicamente en rutas lejanas.

---

### 2. Implementación de Lazy Loading en Vue Router
- Se aplicó el uso de importaciones dinámicas con import() en router/index.js.
- Se mejoró el rendimiento de carga inicial y la eficiencia general del sistema, especialmente en dispositivos móviles.

---

### 3. Optimización de aliases y configuración de jsconfig.json
- Se revisaron y ajustaron todos los alias definidos en vue.config.js.
- Se generó un archivo jsconfig.json en la raíz de vuefrontend para habilitar autocompletado y navegación adecuada en el editor.

---

### 4. Centralización de lógica de autenticación
- Se actualizó el archivo mixins/authMixin.js con dos métodos reutilizables:
  - getAuthenticatedUser()
  - hasPermission(permission)
- Esto permite acceder al usuario autenticado y validar permisos desde cualquier componente.

---

### 5. Verificación de funcionamiento en entorno QA
- Navegación entre vistas funcionando correctamente.
- Modales operativos (Builder, Job, HouseModel).
- Gráficas renderizadas correctamente (AreaChart, BarChart).
- Carga de archivos estáticos sin errores.
- Autenticación y permisos en funcionamiento.
- Consola limpia sin errores visibles.

---

### Estado del sistema
- Listo para pruebas en entorno QA (VPS con Ubuntu).
- Estable, sin errores críticos reportados.
- Cambios aptos para despliegue en producción.
