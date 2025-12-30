import os
import json
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def _build_db_url() -> str:
    """Build SQLAlchemy DB URL.

    Priority:
    1) DATABASE_URL / SQLALCHEMY_DATABASE_URL env var
    2) AWS Secrets Manager JSON pointed by DB_SECRET_NAME (expects keys: host, port, username, password, dbname)
    """
    # 1) Direct env URL
    direct = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URL")
    if direct:
        return direct

    # 2) Secrets Manager
    secret_name = os.getenv("DB_SECRET_NAME")
    if secret_name:
        try:
            import boto3  # type: ignore

            region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
            sm = boto3.client("secretsmanager", region_name=region)
            sec = sm.get_secret_value(SecretId=secret_name)["SecretString"]
            data = json.loads(sec)

            host = data.get("host")
            port = data.get("port", 5432)
            user = data.get("username") or data.get("user")
            pwd = data.get("password")
            dbname = data.get("dbname") or data.get("database")

            if not all([host, user, pwd, dbname]):
                raise ValueError(f"Secret {secret_name} missing required fields")

            # Password may contain special chars, quote it for URL
            return f"postgresql://{quote_plus(str(user))}:{quote_plus(str(pwd))}@{host}:{port}/{dbname}"
        except Exception as e:
            # Fail fast with a clear error (do not log credentials)
            raise RuntimeError(
                "Database configuration error: could not build DB URL from environment or Secrets Manager. "
                "Set DATABASE_URL/SQLALCHEMY_DATABASE_URL or ensure DB_SECRET_NAME is readable and has host/port/username/password/dbname."
            ) from e

    raise RuntimeError(
        "Database configuration error: DATABASE_URL/SQLALCHEMY_DATABASE_URL not set and DB_SECRET_NAME not provided."
    )


engine = create_engine(_build_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()