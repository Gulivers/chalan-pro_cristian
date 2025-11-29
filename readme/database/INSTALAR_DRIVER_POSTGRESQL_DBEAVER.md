# 📦 Cómo Instalar el Driver PostgreSQL JDBC en DBeaver

## 🎯 Ubicación del Archivo JAR

El archivo `postgresql-42.7.8.jar` debe colocarse en el directorio de drivers de DBeaver.

---

## 📍 Paso 1: Ubicación del Driver en DBeaver

### Opción A: Agregar desde DBeaver (RECOMENDADO)

1. **Abre DBeaver**
2. **Ve a:** `Window → Preferences` (o `DBeaver → Preferences` en Mac)
3. **Navega a:** `Connections → Drivers`
4. **Busca:** `PostgreSQL` en la lista de drivers
5. **Selecciona** `PostgreSQL`
6. **Ve a la pestaña:** `Libraries`
7. **Click en:** `Add File` o `Download/Update`
8. **Navega** hasta donde descargaste `postgresql-42.7.8.jar`
9. **Selecciona** el archivo y haz click en `Open`
10. **Click en:** `OK` para guardar

### Opción B: Ubicación Manual del Directorio de Drivers

Si prefieres copiar manualmente el archivo:

#### Windows:
```
C:\Users\[TU_USUARIO]\.dbeaver\drivers\
```

O en ruta alternativa:
```
%APPDATA%\DBeaverData\drivers\
```

#### Mac:
```
~/Library/DBeaverData/drivers/
```

#### Linux:
```
~/.dbeaver/drivers/
```

---

## 🔧 Paso 2: Configurar el Driver PostgreSQL

### 1. Abrir Configuración del Driver

**DBeaver → Preferences → Connections → Drivers → PostgreSQL**

### 2. Pestaña "Settings"

Verifica que tenga:
- **Driver Type:** `PostgreSQL`
- **Driver Name:** `PostgreSQL`
- **Class Name:** `org.postgresql.Driver`
- **URL Template:** `jdbc:postgresql://{host}[:{port}]/[{database}]`
- **Default Port:** `5432`

### 3. Pestaña "Libraries"

Aquí es donde agregas el archivo `postgresql-42.7.8.jar`:

1. **Click en:** `Add File`
2. **Navega** hasta `postgresql-42.7.8.jar`
3. **Selecciona** el archivo
4. **Click en:** `Open`

**O si prefieres descargar directamente desde DBeaver:**

1. **Click en:** `Download/Update`
2. **Selecciona** la versión más reciente (42.7.8)
3. **Click en:** `Download`

### 4. Pestaña "Default properties"

Agrega estas propiedades:

```
ssl=false
sslmode=disable
```

**Cómo agregar:**
1. **Click en:** `Add`
2. **Property name:** `ssl`
3. **Property value:** `false`
4. **Click en:** `Add` de nuevo
5. **Property name:** `sslmode`
6. **Property value:** `disable`
7. **Click en:** `OK`

### 5. Click en `OK` para guardar

---

## ✅ Paso 3: Verificar que el Driver está Instalado

### Verificar Versión del Driver:

1. **Ve a:** `Window → Preferences → Connections → Drivers → PostgreSQL`
2. **Pestaña:** `Libraries`
3. **Debes ver:** `postgresql-42.7.8.jar` en la lista

### Verificar Configuración:

1. **Crea una nueva conexión** o **edita** la existente
2. **Selecciona:** `PostgreSQL` como tipo de base de datos
3. **Click en:** `Test Connection`
4. **Debe mostrar:** El driver correcto en la información

---

## 🚀 Paso 4: Usar el Driver en una Nueva Conexión

### Crear Nueva Conexión:

1. **Click derecho** en `Connections` en el panel izquierdo
2. **Selecciona:** `New Database Connection`
3. **Selecciona:** `PostgreSQL`
4. **Click en:** `Next`

### Configurar Conexión:

```
Host:        127.0.0.1
Port:        5432
Database:    chalan_sch_txn
Username:    chalan_user
Password:    chalan_password
```

5. **Click en:** `Test Connection`
6. **Debe conectarse exitosamente** ✅

---

## 🔍 Verificación Final

### Query para Verificar Versión del Driver:

En DBeaver, después de conectarte, ejecuta:

```sql
SELECT version();
```

**Resultado esperado:**
```
PostgreSQL 16.10 (Debian 16.10-1.pgdg13+1)...
```

Si ves esto, el driver está funcionando correctamente.

---

## 🚨 Solución de Problemas

### Problema 1: No encuentra el archivo JAR

**Solución:**
- Verifica que descargaste el archivo completo
- Asegúrate de que el archivo no esté corrupto
- Descarga nuevamente desde: https://jdbc.postgresql.org/download/

### Problema 2: Driver no aparece en la lista

**Solución:**
1. Cierra y abre DBeaver
2. Ve a Preferences → Drivers
3. Verifica que PostgreSQL esté en la lista

### Problema 3: Error al cargar el driver

**Solución:**
- Verifica que la versión del driver sea compatible (42.2.0 o superior)
- Asegúrate de que solo tengas una versión del driver en la lista
- Elimina versiones antiguas si existen

### Problema 4: Sigue sin conectarse

**Solución:**
1. Verifica que el driver esté en la pestaña Libraries
2. Verifica las propiedades (`ssl=false`, `sslmode=disable`)
3. Prueba con la URL completa en lugar de campos individuales

---

## 📋 Resumen Rápido

1. **Descarga:** `postgresql-42.7.8.jar` desde https://jdbc.postgresql.org/download/
2. **Abre DBeaver:** Window → Preferences → Connections → Drivers → PostgreSQL
3. **Pestaña Libraries:** Click en `Add File` → Selecciona `postgresql-42.7.8.jar`
4. **Pestaña Default properties:** Agrega `ssl=false` y `sslmode=disable`
5. **Click OK:** Guarda los cambios
6. **Prueba conexión:** Crea nueva conexión y prueba

---

## 📁 Estructura de Directorios (Referencia)

```
DBeaver/
└── drivers/
    └── postgresql/
        ├── postgresql-42.7.8.jar  ← AQUÍ va tu archivo
        └── (otros archivos del driver)
```

---

## ✅ Listo

Una vez que agregues el driver `postgresql-42.7.8.jar` en DBeaver y configures las propiedades, deberías poder conectarte correctamente a tu base de datos PostgreSQL local.

