from typing import List, Optional
from pydantic import BaseModel
class UserIdentity(BaseModel):
    principalId: str
class RequestParameters(BaseModel):
    principalId: str
    region: str
    sourceIPAddress: str
class ResponseElements(BaseModel):
    x_amz_id_2: str
    x_amz_request_id: str
    x_minio_deployment_id: str
    x_minio_origin_endpoint: str
class S3Object(BaseModel):
    s3SchemaVersion: str
    configurationId: str
    bucket: dict
    object: dict
class Source(BaseModel):
    host: str
    port: str
    userAgent: str
class Record(BaseModel):
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: str
    eventName: str
    userIdentity: UserIdentity
    requestParameters: RequestParameters
    responseElements: ResponseElements
    s3: S3Object
    source: Source
class Value(BaseModel):
    EventName: str
    Key: str
    Records: List[Record]
class ResumeEvent(BaseModel):
    topic: str
    partition: int
    offset: int
    timestamp: int
    timestamp_type: int
    key: bytes
    value: Value
    headers: List[Optional[str]]
    checksum: Optional[str]
    serialized_key_size: int
    serialized_value_size: int
    serialized_header_size: int