import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def get_db_connection() -> async_sessionmaker:
    """create async session

    Returns:
        async_sessionmaker:async session maker object
    """
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://log_analysis_user:Fq3MdiTt@localhost/log_analysis_db",
    )
    engine = create_async_engine(
        url,
        echo=False,
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    return async_session
