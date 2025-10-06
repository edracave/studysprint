Param(
  [Parameter(Mandatory=$false)][string]$Token = "",
  [Parameter(Mandatory=$false)][string]$BaseUrl = "http://localhost:8000"
)

Write-Host "=== Configurar Webhook de Telegram ==="
if (-not $Token -or $Token -eq "") {
  $Token = Read-Host "Introduce tu TELEGRAM_BOT_TOKEN"
}
$webhookUrl = "$BaseUrl/telegram/webhook"
Write-Host ("Usando URL: {0}" -f $webhookUrl)

try {
  $response = Invoke-WebRequest -Method POST -Uri ("https://api.telegram.org/bot{0}/setWebhook" -f $Token) -Body @{ url = $webhookUrl }
  Write-Host "Respuesta Telegram:"
  $response.Content
} catch {
  Write-Host "Error configurando webhook:"
  Write-Host $_.Exception.Message
}
