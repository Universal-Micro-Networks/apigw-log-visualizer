import datetime
import uuid

from sqlalchemy import (
    BIGINT,
    INTEGER,
    TIMESTAMP,
    UUID,
    BigInteger,
    Identity,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from packages.log_collection.infra.model.base import Base


class AccessLog(Base):
    __tablename__ = "access_logs"
    __table_args__ = (
        Index("api_key_id_idx", "api_key_id"),
        Index("request_time_epoch_idx", "request_time_epoch"),
        Index("stage_idx", "stage"),
        Index("status_idx", "status"),
        Index("response_latency_idx", "response_latency"),
    )
    id: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1, cycle=False), primary_key=True
    )
    request_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    api_key: Mapped[str] = mapped_column(String, nullable=False)
    api_key_id: Mapped[str] = mapped_column(String, nullable=False)
    request_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    request_time_epoch: Mapped[int] = mapped_column(BIGINT, nullable=False)
    api_id: Mapped[str] = mapped_column(String, nullable=False)
    stage: Mapped[str] = mapped_column(String, nullable=False)
    http_method: Mapped[str] = mapped_column(String, nullable=False)
    protocol: Mapped[str] = mapped_column(String, nullable=False)
    domain_name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    resource_path: Mapped[str] = mapped_column(String, nullable=False)
    user_agent: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[int] = mapped_column(INTEGER, nullable=False)
    response_latency: Mapped[int] = mapped_column(INTEGER, nullable=False)
    error_message: Mapped[str] = mapped_column(String, nullable=False)
    response_type: Mapped[str] = mapped_column(String, nullable=False)
    response_length: Mapped[int] = mapped_column(INTEGER, nullable=False)
    integration_status: Mapped[int] = mapped_column(INTEGER, nullable=False)
    integration_latency: Mapped[int] = mapped_column(INTEGER, nullable=False)
    integration_error: Mapped[str] = mapped_column(String, nullable=False)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    caller: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[str] = mapped_column(String, nullable=False)
