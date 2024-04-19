import datetime
import uuid

from pydantic import BaseModel


class ApigwLog(BaseModel):
    request_id: uuid.UUID
    api_key: str
    api_key_id: str
    request_time: datetime.datetime
    request_time_epoch: int
    api_id: str
    stage: str
    http_method: str
    protocol: str
    domain_name: str
    path: str
    resource_path: str
    user_agent: str
    status: str
    response_latency: int
    error_message: str
    response_type: str
    response_length: int
    integration_status: int
    integration_latency: int
    integration_error: str
    ip: str
    caller: str
    user: str

    @classmethod
    def new(
        cls,
        request_id: uuid.UUID,
        api_key: str,
        api_key_id: str,
        request_time: datetime.datetime,
        request_time_epoch: int,
        api_id: str,
        stage: str,
        http_method: str,
        protocol: str,
        domain_name: str,
        path: str,
        resource_path: str,
        user_agent: str,
        status: str,
        response_latency: int,
        error_message: str,
        response_type: str,
        response_length: int,
        integration_status: int,
        integration_latency: int,
        integration_error: str,
        ip: str,
        caller: str,
        user: str,
    ) -> "ApigwLog":
        return ApigwLog(
            request_id=request_id,
            api_key=api_key,
            api_key_id=api_key_id,
            request_time=request_time,
            request_time_epoch=request_time_epoch,
            api_id=api_id,
            stage=stage,
            http_method=http_method,
            protocol=protocol,
            domain_name=domain_name,
            path=path,
            resource_path=resource_path,
            user_agent=user_agent,
            status=status,
            response_latency=response_latency,
            error_message=error_message,
            response_type=response_type,
            response_length=response_length,
            integration_status=integration_status,
            integration_latency=integration_latency,
            integration_error=integration_error,
            ip=ip,
            caller=caller,
            user=user,
        )
