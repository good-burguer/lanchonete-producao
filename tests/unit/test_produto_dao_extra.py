import pytest
from types import SimpleNamespace
from decimal import Decimal

from app.dao.produto_dao import ProdutoDAO


def test_atualizar_produto_updates_and_refresh(monkeypatch):
    # fake existing product
    existing = SimpleNamespace(id=1, nome="Old", descricao="d", preco=Decimal("1.00"), categoria=1)

    class FakeDAO(ProdutoDAO):
        def __init__(self):
            self._produto = existing

        def buscar_por_id(self, id):
            return self._produto if id == 1 else None

        def __getattr__(self, name):
            # delegate to base when needed
            raise AttributeError

    dao = ProdutoDAO(db_session=None)
    dao.buscar_por_id = lambda id: existing

    new_data = SimpleNamespace(nome="New", descricao="nd", preco=Decimal("2.00"), categoria=2)

    # monkeypatch commit/refresh methods on dao.db_session
    class FakeSession:
        def commit(self):
            pass

        def refresh(self, obj):
            pass

    dao.db_session = FakeSession()

    updated = dao.atualizar_produto(1, new_data)

    assert updated.nome == "New"
    assert str(updated.preco) == str(Decimal("2.00"))
