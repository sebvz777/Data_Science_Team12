# Extract the filename
filename="sicherheitsleitlinie.pdf"

# Encode the PDF file without newlines
base64_pdf=$(base64 -w 0 $filename)

# Send the data to Elasticsearch using a POST request
curl.exe -X POST "localhost:9200/test5/_doc/my_id?pipeline=attachment&pretty" -H 'Content-Type: application/json' --data-binary @- <<DATA
{
  "data": "$base64_pdf",
  "filename": "$filename"
}
DATA
