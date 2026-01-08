import importlib
import json


def test_build_db_url_with_secret(monkeypatch):
    # Simula o secrets manager retornando credenciais
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SQLALCHEMY_DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_SECRET_NAME", "mysecret")

    class FakeSM:
        def __init__(self, **kwargs):
            pass

        def get_secret_value(self, SecretId):
            return {"SecretString": json.dumps({
                "host": "db.local",
                "port": 5432,
                "username": "user",
                "password": "pass",
                "dbname": "mydb"
            })}

    def fake_boto3_client(name, region_name=None):
        return FakeSM()

    monkeypatch.setenv("AWS_REGION", "us-east-1")

    import builtins
    import sys

    # Patch boto3 client used inside module
    import types
    fake_boto3 = types.SimpleNamespace(client=fake_boto3_client)

    import importlib
    mod = importlib.import_module("app.infrastructure.db.database")
    # inject fake boto3 into module globals and reload
    mod.boto3 = fake_boto3
    importlib.reload(mod)

    url = mod._build_db_url()
    assert url.startswith("postgresql://")
    assert "user" in url and "pass" in url and "mydb" in url


def test_build_db_url_secret_missing_fields(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SQLALCHEMY_DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_SECRET_NAME", "mysecret")

    class FakeSMBad:
        def get_secret_value(self, SecretId):
            return {"SecretString": json.dumps({"host": "db.local"})}

    def fake_boto3_client(name, region_name=None):
        return FakeSMBad()

    import importlib, types
    mod = importlib.import_module("app.infrastructure.db.database")
    mod.boto3 = types.SimpleNamespace(client=fake_boto3_client)
    importlib.reload(mod)

    try:
        mod._build_db_url()
        assert False, "Expected RuntimeError"
    except RuntimeError:
        assert True
