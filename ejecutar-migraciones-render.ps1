# Script para ejecutar migraciones en Render usando SSH
# Requiere tener configurada la clave SSH para Render

Write-Host "=== Ejecutar Migraciones en Render ===" -ForegroundColor Cyan
Write-Host ""

# Información del servicio
$SERVICE_ID = "srv-d44nroripnbc73angjdg"
$SSH_ADDRESS = "${SERVICE_ID}@ssh.oregon.render.com"

Write-Host "Servicio: chalan-backend" -ForegroundColor Yellow
Write-Host "SSH Address: $SSH_ADDRESS" -ForegroundColor Yellow
Write-Host ""

# Opción 1: Ejecutar migraciones vía SSH
Write-Host "Opción 1: Ejecutar migraciones vía SSH" -ForegroundColor Green
Write-Host "Ejecuta el siguiente comando en tu terminal:" -ForegroundColor White
Write-Host ""
Write-Host "# Para multi-tenant (schema compartido):" -ForegroundColor Yellow
Write-Host "ssh $SSH_ADDRESS 'cd /opt/render/project/src && python manage.py migrate_schemas --shared'" -ForegroundColor Cyan
Write-Host ""
Write-Host "# O para migraciones estándar:" -ForegroundColor Yellow
Write-Host "ssh $SSH_ADDRESS 'cd /opt/render/project/src && python manage.py migrate'" -ForegroundColor Cyan
Write-Host ""

# Opción 2: Usar el Shell de Render (Recomendado)
Write-Host "Opción 2: Usar el Shell de Render (Recomendado)" -ForegroundColor Green
Write-Host "1. Ve a: https://dashboard.render.com/web/$SERVICE_ID" -ForegroundColor White
Write-Host "2. Haz clic en 'Shell' en el menú lateral" -ForegroundColor White
Write-Host "3. Ejecuta uno de estos comandos:" -ForegroundColor White
Write-Host "   - Para multi-tenant: python manage.py migrate_schemas --shared" -ForegroundColor Cyan
Write-Host "   - Para verificar: python manage.py showmigrations" -ForegroundColor Cyan
Write-Host "   - Migración estándar: python manage.py migrate" -ForegroundColor Cyan
Write-Host ""

# Opción 3: Verificar migraciones pendientes
Write-Host "Opción 3: Verificar migraciones pendientes" -ForegroundColor Green
Write-Host "Ejecuta: python manage.py showmigrations" -ForegroundColor White
Write-Host ""

# Nota sobre migraciones automáticas
Write-Host "Nota: Las migraciones se ejecutan automáticamente en cada despliegue" -ForegroundColor Yellow
Write-Host "según la configuración en render.yaml (startCommand)." -ForegroundColor Yellow
Write-Host ""

# Verificar si hay un despliegue reciente
Write-Host "¿Quieres verificar el estado del último despliegue?" -ForegroundColor Cyan
Write-Host "Ve a: https://dashboard.render.com/web/$SERVICE_ID/logs" -ForegroundColor White
Write-Host ""

