import requests
from datetime import timedelta
from minioClient import client

# Define the URL of the PDF file
# pdf_url = 'http://minio.minio-operator.svc.cluster.local/armss-dev/index.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=4W1T08P4FVK2JV10A78P%2F20240419%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240419T051629Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0VzFUMDhQNEZWSzJKVjEwQTc4UCIsImV4cCI6MTcxMzUwNjQ5MCwicGFyZW50IjoiYXJtc3MifQ.R9yMUbDVGI4wDLkhp7XkskAeTK1tHH7MNNpwW3jV2CqwFGMqWInYsRrlFq2ENAO_47Frioz8sMhfg7jbWLhfhg&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=5faf9ea63fb93c8a6e3b7d3afd385a39ebf3f0e9ca1e2e2aac6681daba94e070'
# Define the path where the PDF file will be saved
output_path = "index.html"

pdf_url = client.get_presigned_url(
        "GET",
        "armss-dev",
        'index.html',
        expires=timedelta(days=1),
    )

# Send a GET request to the URL
response = requests.get(pdf_url)

# Check if the request was successful
if response.status_code == 200:
    # Write the content of the response to a file
    with open(output_path, "wb") as file:
        file.write(response.content)
    print(f"File saved as {output_path}")
else:
    print(f"Failed to download file. HTTP Status code: {response.status_code}")

