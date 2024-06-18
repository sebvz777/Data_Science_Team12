# Extract the filename
$filename = "C:\Users\rober\Documents\Data_Sience_Team12\tests\Richtline_Lenkung_von_Dokumenten_L.pdf"

# Encode the PDF file without newlines
$base64_pdf = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($filename))

# Create JSON data
$jsonPayload = @{
    data = $base64_pdf
    filename = $filename
} | ConvertTo-Json -Compress

# Send the data to Elasticsearch using a POST request
Invoke-RestMethod -Method Post -Uri "http://localhost:9200/test10/_doc/3?pipeline=attachment&pretty" -ContentType "application/json" -Body $jsonPayload
