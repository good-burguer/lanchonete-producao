from types import SimpleNamespace
from decimal import Decimal
import pytest

from app.dao.produto_dao import ProdutoDAO


def test_criar_produto_calls_session_methods(monkeypatch):
    class FakeSession:
        def __init__(self):
            self.add_called = False
            self.commit_called = False
            self.refreshed = None

        def add(self, obj):
            self.add_called = True

        def commit(self):
            self.commit_called = True

        def refresh(self, obj):
            self.refreshed = obj

    fake_session = FakeSession()
    dao = ProdutoDAO(fake_session)

    produto_in = SimpleNamespace(nome="X", descricao="d", preco=Decimal("5.00"), categoria=1)
    result = dao.criar_produto(produto_in)

    assert fake_session.add_called is True
    assert fake_session.commit_called is True
    assert result.nome == "X"


def test_deletar_produto_raises_when_not_found():
    dao = ProdutoDAO(db_session=None)
    dao.buscar_por_id = lambda id: None

    with pytest.raises(ValueError):
        dao.deletar_produto(123)
