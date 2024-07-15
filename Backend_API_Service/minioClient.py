from minio import Minio
from decouple import config

access_keys=config('MINIO_access_key')
secret_keys=config('MINIO_secret_key')
minio_endpoint=config('MINIO_endpoint')
minio_secure = config('MINIO_SECURE')

# client = Minio(
#     "minio-endpoint.skilldify.ai", 
#     access_key=access_keys,
#     secret_key=secret_keys,
#     secure=False 

# )

client = Minio(
    minio_endpoint,
    access_key=access_keys,
    secret_key=secret_keys,
    secure=minio_secure
)
