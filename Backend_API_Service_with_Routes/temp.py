import requests
url = "http://minio:9000/resumebucket/DifferentRoles.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=xeLzrgnQKbkS49DeeuTB%2F20240419%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240419T055856Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=776c0a0bc8e9130812ecfaa018d2e28ae11bb7aeadab523914b9d8615c25c2aa"
response = requests.get(url)
with open("DifferentRoles.pdf", "wb") as file:
    file.write(response.content)
print("File downloaded successfully.")