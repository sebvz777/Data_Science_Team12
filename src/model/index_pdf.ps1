# Extract the filename
$filename = "C:\Users\rober\Documents\Data_Sience_Team12\tests\Risikoanalyse_L.pdf"

# Encode the PDF file without newlines
$base64_pdf = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($filename))

# Create JSON data
$jsonPayload = @{
    data = $base64_pdf
    filename = $filename
} | ConvertTo-Json -Compress

# Send the data to Elasticsearch using a POST request
Invoke-RestMethod -Method Post -Uri "http://localhost:9200/test11/_doc/1?pipeline=attachment&pretty" -ContentType "application/json" -Body $jsonPayload
