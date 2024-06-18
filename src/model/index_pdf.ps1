# Extract the filename
$filename = "src\model\Sicherheitsleitlinie_L.pdf"

# Encode the PDF file without newlines
$base64_pdf = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($filename))

# Create JSON data
$jsonPayload = @{
    data = $base64_pdf
    filename = $filename
} | ConvertTo-Json -Compress

# Send the data to Elasticsearch using a POST request
Invoke-RestMethod -Method Post -Uri "http://localhost:9200/test7/_doc/my_id?pipeline=attachment&pretty" -ContentType "application/json" -Body $jsonPayload
