from decimal import Decimal
import pytest
from fastapi import HTTPException

from app.api import produto as produto_api
from app.adapters.dto.produto_dto import ProdutoCreateSchema


def make_fake_produto(id=1, nome="X", preco=Decimal("9.99")):
    return {
        "id": id,
        "nome": nome,
        "descricao": None,
        "preco": preco,
        "categoria": {"id": 1, "nome": "Bebida"}
    }


def test_criar_produto_success(monkeypatch):
    class FakeController:
        def __init__(self, db_session):
            pass

        def criar_produto(self, produto_data):
            return {"status": "success", "data": make_fake_produto(1, produto_data.nome, produto_data.preco)}

    monkeypatch.setattr(produto_api, "ProdutoController", FakeController)

    schema = ProdutoCreateSchema(nome="X-Burger", descricao="desc", categoria=1, preco=Decimal("9.99"))
    res = produto_api.criar_produto(schema, gateway=None)

    assert res["status"] == "success"
    assert res["data"]["nome"] == "X-Burger"


def test_buscar_produto_not_found(monkeypatch):
    class FakeController:
        def __init__(self, db_session):
            pass

        def buscar_produto(self, id):
            raise ValueError("Produto não encontrado")

    monkeypatch.setattr(produto_api, "ProdutoController", FakeController)

    with pytest.raises(HTTPException) as exc:
        produto_api.buscar_produto(999, gateway=None)

    assert exc.value.status_code == 404
