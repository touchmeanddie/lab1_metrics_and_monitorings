1..30 | ForEach-Object {
    Invoke-RestMethod -Uri "http://localhost:8080/orders" -Method Post -ContentType "application/json" -Body '{"amount": 100, "items_count": 1}' | Out-Null
    Start-Sleep -Milliseconds 2000
}