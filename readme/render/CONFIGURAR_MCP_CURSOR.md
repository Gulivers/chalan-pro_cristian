# 🔧 Configurar MCP (Model Context Protocol) en Cursor para Render.com

## 📋 Requisitos Previos

1. **Cuenta de Render.com** activa
2. **API Key de Render.com** (necesaria para la autenticación)

## 🔑 Paso 1: Obtener API Key de Render.com

1. Inicia sesión en [Render.com](https://dashboard.render.com)
2. Ve a **Account Settings** → **API Keys**
3. Haz clic en **Create API Key**
4. Dale un nombre descriptivo (ej: "Cursor MCP")
5. **Copia la API Key** (solo se muestra una vez)

## ⚙️ Paso 2: Configurar MCP en Cursor

### Opción A: Configuración Manual (Recomendada)

1. Abre Cursor
2. Ve a **Settings** (⚙️) → **Features** → **Model Context Protocol**
3. O abre directamente el archivo de configuración:
   - **Windows**: `%APPDATA%\Cursor\User\globalStorage\mcp.json`
   - **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/mcp.json`
   - **Linux**: `~/.config/Cursor/User/globalStorage/mcp.json`

4. Agrega la siguiente configuración:

```json
{
  "mcpServers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer [tu-api-key-aqui]"
      }
    }
  }
}
```

5. Reemplaza `"tu-api-key-aqui"` con tu API Key de Render.com
6. Guarda el archivo
7. **Reinicia Cursor** para que los cambios surtan efecto

### Opción B: Usar Variables de Entorno

Si prefieres no guardar la API key en el archivo de configuración:

1. Configura la variable de entorno en tu sistema:
   - **Windows PowerShell**:
     ```powershell
     [System.Environment]::SetEnvironmentVariable('RENDER_API_KEY', 'tu-api-key-aqui', 'User')
     ```
   - **macOS/Linux**:
     ```bash
     export RENDER_API_KEY="tu-api-key-aqui"
     # Agregar a ~/.bashrc o ~/.zshrc para persistencia
     ```

2. En el archivo de configuración MCP, usa:
```json
{
  "mcpServers": {
    "render": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-render"
      ],
      "env": {
        "RENDER_API_KEY": "${RENDER_API_KEY}"
      }
    }
  }
}
```

## ✅ Paso 3: Verificar la Conexión

1. Reinicia Cursor
2. Abre el chat con el asistente
3. Pregunta: "¿Puedes listar mis servicios en Render?"
4. Si funciona correctamente, deberías ver tus servicios de Render

## 🚀 Paso 4: Usar MCP para Crear Ambientes

Una vez configurado, puedes pedirme que:
- Liste tus servicios actuales
- Cree nuevas bases de datos PostgreSQL
- Cree nuevos servicios web
- Configure variables de entorno
- Y más operaciones de Render.com

## 📝 Notas Importantes

- **Seguridad**: Nunca compartas tu API Key públicamente
- **Permisos**: Asegúrate de que tu API Key tenga los permisos necesarios
- **Límites**: Respeta los límites de la API de Render.com
- **Workspace**: El MCP seleccionará automáticamente tu workspace de Render

## 🔍 Solución de Problemas

### Error: "No workspace set"
- Verifica que tu API Key sea válida
- Asegúrate de tener al menos un workspace en Render.com

### Error: "Connection failed"
- Verifica que la API Key esté correctamente configurada
- Revisa que Cursor tenga acceso a internet
- Intenta reiniciar Cursor

### No aparecen las herramientas MCP
- Verifica que el archivo de configuración tenga la sintaxis correcta (JSON válido)
- Reinicia Cursor completamente
- Verifica que el paquete `@modelcontextprotocol/server-render` esté disponible

## 📚 Referencias

- [Documentación de Render API](https://render.com/docs/api)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Cursor MCP Documentation](https://docs.cursor.com/)

