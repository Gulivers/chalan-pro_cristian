# 🔧 Solución Definitiva: Error de Contraseña en DBeaver/Navicat

## ❌ El Error

```
FATAL: password authentication failed for user "chalan_user"
```

## ✅ Solución Inmediata

### Paso 1: Verifica que escribes la contraseña EXACTA

**Credenciales CORRECTAS para DBeaver/Navicat:**

```
Host:        127.0.0.1 (NO localhost)
Puerto:      5432
Usuario:     chalan_user
Contraseña:  chalan_password  ← ESCRIBE ESTA EXACTA
Base de Datos: chalan_sch_txn
```

### Paso 2: Limpia la contraseña guardada en DBeaver

1. En DBeaver, ve a la conexión que estás probando
2. Click derecho → **Edit Connection**
3. **DESMARCA** "Save password" temporalmente
4. Escribe la contraseña manualmente: `chalan_password`
5. Marca "Save password" de nuevo
6. Prueba la conexión

### Paso 3: Si sigue fallando, resetea la contraseña

Ejecuta este comando en PowerShell:

```powershell
docker exec chalan_postgres psql -U postgres -c "ALTER USER chalan_user WITH PASSWORD 'chalan_password';"
```

### Paso 4: Usa el usuario de migración (alternativa)

Si `chalan_user` sigue dando problemas, usa el usuario `migracion_user`:

```
Host:        127.0.0.1
Puerto:      5432
Usuario:     migracion_user
Contraseña:  migracion_password123
Base de Datos: chalan_sch_txn
```

---

## 🔍 Verificación de Diagnóstico

### Prueba la conexión desde terminal:

```powershell
# Probar conexión con chalan_user
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_user, current_database();"

# Debería mostrar:
#  current_user | current_database 
# --------------+------------------
#  chalan_user  | chalan_sch_txn
```

Si esto funciona pero DBeaver no, el problema es que DBeaver está usando una contraseña incorrecta.

---

## 🚨 Errores Comunes

### Error 1: Usas "localhost" en lugar de "127.0.0.1"
**Solución:** Cambia a `127.0.0.1` en DBeaver

### Error 2: Contraseña con espacios o caracteres especiales
**Solución:** Copia y pega exactamente: `chalan_password`

### Error 3: Contraseña guardada incorrectamente en DBeaver
**Solución:** 
1. Elimina la conexión en DBeaver
2. Crea una nueva conexión
3. Escribe la contraseña manualmente

### Error 4: Mayúsculas/minúsculas
**Solución:** Usa exactamente: `chalan_user` (todo minúsculas) y `chalan_password` (todo minúsculas)

---

## ✅ Verificación Final

Después de aplicar la solución, deberías poder:

1. ✅ Conectarte desde DBeaver
2. ✅ Ver todas las tablas en `chalan_sch_txn`
3. ✅ Ejecutar queries SQL
4. ✅ Importar datos desde CSV

---

## 📞 Si Nada Funciona

Ejecuta este script completo de diagnóstico:

```powershell
# 1. Verificar contenedor corriendo
docker ps --filter "name=chalan_postgres"

# 2. Resetear contraseña
docker exec chalan_postgres psql -U postgres -c "ALTER USER chalan_user WITH PASSWORD 'chalan_password';"

# 3. Probar conexión
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT 'CONEXION OK' as estado;"

# 4. Ver usuarios
docker exec chalan_postgres psql -U postgres -c "\du"
```

Si el paso 3 funciona pero DBeaver no, el problema está en DBeaver, no en PostgreSQL.

