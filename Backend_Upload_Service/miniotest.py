from minioClient import client
from minio.error import S3Error
from datetime import  timedelta

try:
    url = client.get_presigned_url(
            "PUT",
            "armss-dev",
            'out.log',
            expires=timedelta(days=1),

        )
    print(url)
except S3Error as e:
    print(f"An error occurred: {e}")


