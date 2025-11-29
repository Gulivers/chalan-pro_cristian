# 🔧 Solución: Problema de Driver o Autenticación en DBeaver

## ✅ Verificación del Driver

El driver que estás usando parece correcto:
- **Class Name:** `org.postgresql.Driver` ✅
- **URL Template:** `jdbc:postgresql://{host}[:{port}]/[{database}]` ✅
- **Thread safe driver:** Marcado ✅

**PERO** puede haber problemas con la versión del driver o la configuración de autenticación.

---

## 🔧 Soluciones para Problemas de Driver

### Solución 1: Actualizar el Driver de PostgreSQL en DBeaver

1. En DBeaver, ve a **Window → Preferences → Drivers → PostgreSQL**
2. Click en **Download** para descargar la última versión del driver
3. O manualmente:
   - Click en **Edit Driver**
   - En la pestaña **Libraries**, verifica que tengas una versión reciente
   - Si no, agrega manualmente: `https://jdbc.postgresql.org/download.html`
   - Descarga la versión más reciente (ej: `postgresql-42.7.1.jar`)

### Solución 2: Ajustar Propiedades del Driver

En la ventana "Edit Driver 'PostgreSQL'", ve a la pestaña **"Default properties"** y agrega:

```
ssl=false
sslmode=disable
```

O en la pestaña **"Advanced parameters"**, agrega:
```
useSSL=false
```

### Solución 3: Verificar Método de Autenticación

En la ventana de conexión, en la sección **Authentication**, verifica:
- **Authentication:** Debe ser `Database Native` (no "No authentication")
- **Username:** `chalan_user`
- **Password:** `chalan_password`

---

## 🔍 Diagnóstico Avanzado

### Prueba 1: Verificar que la conexión funciona desde terminal

```powershell
# Esto DEBE funcionar
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_user;"
```

Si esto funciona pero DBeaver no, el problema es específico de DBeaver/Driver.

### Prueba 2: Verificar método de autenticación de PostgreSQL

```powershell
docker exec chalan_postgres psql -U postgres -c "SHOW password_encryption;"
```

Debería mostrar `scram-sha-256`.

### Prueba 3: Conectar usando URL completa en DBeaver

En lugar de usar los campos individuales, prueba usar la **URL completa**:
1. En DBeaver, en la sección **Connect by**, selecciona **URL** (no "Host")
2. Usa esta URL exacta:
```
jdbc:postgresql://127.0.0.1:5432/chalan_sch_txn?user=chalan_user&password=chalan_password
```

**⚠️ Nota:** Esto es solo para prueba. Si funciona, el problema es la configuración de autenticación en DBeaver.

---

## ⚙️ Configuración Recomendada del Driver

### En DBeaver, configura el driver así:

1. **Settings:**
   - Driver Type: `PostgreSQL`
   - Class Name: `org.postgresql.Driver`
   - URL Template: `jdbc:postgresql://{host}[:{port}]/[{database}]`
   - Default Port: `5432`

2. **Default properties** (agrega estas propiedades):
   ```
   ssl=false
   sslmode=disable
   ```

3. **Advanced parameters** (opcional):
   ```
   connectTimeout=10
   socketTimeout=10
   ```

---

## 🔄 Alternativa: Usar pgAdmin en lugar de DBeaver

Si DBeaver sigue dando problemas, puedes usar pgAdmin que ya está configurado:

1. Abre el navegador
2. Ve a: `http://localhost:5050`
3. Login con:
   - Email: `admin@chalan.com`
   - Password: (la misma que `POSTGRES_PASSWORD` en tu `.env`)
4. Agregar servidor:
   - Host: `chalan_postgres` (nombre del contenedor)
   - Port: `5432`
   - Database: `chalan_sch_txn`
   - Username: `chalan_user`
   - Password: `chalan_password`

---

## 🚨 Si Nada Funciona

### Solución Final: Resetear completamente la autenticación

```powershell
# 1. Resetear contraseña
docker exec chalan_postgres psql -U postgres -c "ALTER USER chalan_user WITH PASSWORD 'chalan_password';"

# 2. Forzar reconexión (reiniciar contenedor)
docker restart chalan_postgres

# 3. Esperar a que esté listo
docker ps --filter "name=chalan_postgres" --format "table {{.Names}}\t{{.Status}}"

# 4. Probar conexión
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT 'OK' as estado;"
```

---

## 📋 Checklist de Verificación

- [ ] Driver PostgreSQL actualizado en DBeaver
- [ ] Properties del driver configuradas (`ssl=false`)
- [ ] Usuario: `chalan_user`
- [ ] Contraseña: `chalan_password` (escrita manualmente)
- [ ] Host: `127.0.0.1` (NO localhost)
- [ ] Puerto: `5432`
- [ ] Base de datos: `chalan_sch_txn`
- [ ] Authentication: `Database Native`
- [ ] Conexión funciona desde terminal con `psql`

Si todo esto está correcto y sigue fallando, puede ser un bug específico de DBeaver con tu versión de PostgreSQL. En ese caso, usa **pgAdmin** o **psql** directamente.

