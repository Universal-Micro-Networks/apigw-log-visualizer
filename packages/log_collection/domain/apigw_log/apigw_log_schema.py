"""
This module contains the ApigwLog domain model.
"""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApigwLogSchema(BaseModel):
    """
    This class represents the ApigwLog domain model.

    Args:
        BaseModel (_type_): pydantic BaseModel
    """

    model_config = ConfigDict(alias_generator=to_camel)
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
    status: int
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
        status: int,
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
    ) -> "ApigwLogSchema":
        """_summary_

        Args:
            request_id (uuid.UUID): Amazon API Gateway request ID
            api_key (str): API key
            api_key_id (str): API key ID, cf. https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-key-set-up.html
            request_time (datetime.datetime): Request time
            request_time_epoch (int): Request time in Unix Time
            api_id (str): API Gateway ID
            stage (str): API deployed stage
            http_method (str): HTTP method
            protocol (str): Protocol
            domain_name (str): FQDN
            path (str): API Path
            resource_path (str): Resource path
            user_agent (str): User Agent in HTTP Header
            status (str): HTTP status code
            response_latency (int): Response latency in ms
            error_message (str): Error message
            response_type (str): Response type
            response_length (int): Response length
            integration_status (int): Integration status
            integration_latency (int): Integration latency in ms
            integration_error (str): Integration error message
            ip (str): Client IP address
            caller (str): Caller
            user (str): User

        Returns:
            ApigwLog: ApiGwLog object
        """
        return ApigwLogSchema(
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
