# Script para ejecutar migraciones en Render vía SSH
# Requiere tener configurada la clave SSH para Render

$SERVICE_ID = "srv-d44nroripnbc73angjdg"
$SSH_ADDRESS = "${SERVICE_ID}@ssh.oregon.render.com"
$SSH_KEY = "$env:USERPROFILE\.ssh\id_ed25519_render"

Write-Host "=== Ejecutar Migraciones en Render vía SSH ===" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe la clave SSH
if (-not (Test-Path $SSH_KEY)) {
    Write-Host "❌ No se encontró la clave SSH en: $SSH_KEY" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para configurar SSH:" -ForegroundColor Yellow
    Write-Host "1. Ve a: https://dashboard.render.com/account/keys" -ForegroundColor White
    Write-Host "2. Agrega tu clave pública SSH" -ForegroundColor White
    Write-Host "3. La clave debe estar en: $SSH_KEY" -ForegroundColor White
    Write-Host ""
    Write-Host "O usa el Shell de Render directamente:" -ForegroundColor Yellow
    Write-Host "https://dashboard.render.com/web/$SERVICE_ID" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Clave SSH encontrada: $SSH_KEY" -ForegroundColor Green
Write-Host ""
Write-Host "SSH Address: $SSH_ADDRESS" -ForegroundColor Yellow
Write-Host ""

# Comandos a ejecutar
$commands = @(
    "echo '=== Verificando estado de migraciones ==='",
    "cd /opt/render/project/src",
    "python manage.py showmigrations | head -20",
    "",
    "echo '=== Resolviendo conflicto de dependencias ==='",
    "python manage.py migrate appinventory 0002 --fake",
    "",
    "echo '=== Aplicando todas las migraciones ==='",
    "python manage.py migrate_schemas --shared",
    "",
    "echo '=== Verificando resultado ==='",
    "python manage.py showmigrations | head -20"
)

Write-Host "Comandos que se ejecutarán:" -ForegroundColor Yellow
Write-Host ""
foreach ($cmd in $commands) {
    if ($cmd -ne "") {
        Write-Host "  $cmd" -ForegroundColor Gray
    }
}
Write-Host ""

$confirm = Read-Host "¿Deseas ejecutar estos comandos vía SSH? (S/N)"

if ($confirm -ne "S" -and $confirm -ne "s") {
    Write-Host "Operación cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Conectando vía SSH..." -ForegroundColor Cyan

# Construir el comando SSH
$sshCommand = $commands -join " && "

try {
    # Ejecutar comandos vía SSH
    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_ADDRESS $sshCommand
    
    Write-Host ""
    Write-Host "✅ Comandos ejecutados exitosamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verifica el resultado arriba. Si hay errores, ejecuta manualmente:" -ForegroundColor Yellow
    Write-Host "ssh -i $SSH_KEY $SSH_ADDRESS" -ForegroundColor Cyan
    
} catch {
    Write-Host ""
    Write-Host "❌ Error al ejecutar comandos vía SSH" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternativa: Usa el Shell de Render directamente:" -ForegroundColor Yellow
    Write-Host "https://dashboard.render.com/web/$SERVICE_ID" -ForegroundColor Cyan
}

