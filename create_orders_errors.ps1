1..150 | ForEa
ch-Object {
    if ($_ % 5 -eq 0) {
        $body = '{"amount": -100, "items_count": 1}'
    } else {
        $body = '{"amount": 100, "items_count": 1}'
    }

    try {
        Invoke-RestMethod -Uri "http://localhost:8080/orders" -Method Post -ContentType "application/json" -Body $body | Out-Null
    } catch {
    }

    Start-Sleep -Milliseconds 100
}