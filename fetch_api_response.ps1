$headers = @{ Authorization = 'Bearer dev_token_123_fixo' }
$uri = 'https://html.testes.net.br/cron/api.php?edital=12&filtro=solicitacoes'
$outputPath = Join-Path $PSScriptRoot 'api_response_edital_12.json'

$response = Invoke-WebRequest -Method Post -Uri $uri -Headers $headers -UseBasicParsing
[System.IO.File]::WriteAllText($outputPath, $response.Content, [System.Text.UTF8Encoding]::new($false))

Write-Output "Resposta salva em: $outputPath"
