# Extract the filename
filename="C:\Users\rober\Documents\Data_Sience_Team12\src\model\sicherheitsleitlinie.pdf"

# Encode the PDF file without newlines
base64_pdf=$(base64 -w 0 "$filename" | tr -d '\r\n')

# Send the data to Elasticsearch using a POST request
curl -X POST "localhost:9200/test5/_doc/my_id?pipeline=attachment&pretty" -H 'Content-Type: application/json' --data-binary @- <<DATA
{
  "data": "$base64_pdf",
  "filename": "$filename"
}
DATA
