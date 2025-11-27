import pytest
from unittest.mock import MagicMock

from app.gateways.produto_gateway import ProdutoGateway
from app.dao.produto_dao import ProdutoDAO
from app.models.produto import Produto
from app.adapters.enums.categoria_produto import CategoriaProdutoEnum


@pytest.fixture
def mock_db():

    return MagicMock()


@pytest.fixture
def gateway(mock_db, monkeypatch):
    mock_dao = MagicMock(spec=ProdutoDAO)

    monkeypatch.setattr(
        "app.gateways.produto_gateway.ProdutoDAO",
        lambda session: mock_dao
    )

    gateway = ProdutoGateway(db_session=mock_db)
    gateway.dao = mock_dao

    return gateway


def test_criar_produto(gateway):
    produto = Produto(id=1, nome="Teste", preco=10.00)

    gateway.dao.criar_produto.return_value = produto

    result = gateway.criar_produto(produto)

    gateway.dao.criar_produto.assert_called_once_with(produto)
    assert result == produto


def test_listar_todos(gateway):
    produtos = [
        Produto(id=1, nome="A", preco=10.00),
        Produto(id=2, nome="B", preco=20.00),
    ]

    gateway.dao.listar_todos.return_value = produtos

    result = gateway.listar_todos()

    gateway.dao.listar_todos.assert_called_once()
    assert result == produtos
    assert len(result) == 2


def test_listar_por_categoria(gateway):
    categoria = CategoriaProdutoEnum.Lanche
    produtos = [Produto(id=1, nome="X", preco=12)]

    gateway.dao.listar_por_categoria.return_value = produtos

    result = gateway.listar_por_categoria(categoria)

    gateway.dao.listar_por_categoria.assert_called_once_with(categoria)
    assert result == produtos


def test_buscar_por_id(gateway):
    produto = Produto(id=1, nome="Teste", preco=15)

    gateway.dao.buscar_por_id.return_value = produto

    result = gateway.buscar_por_id(1)

    gateway.dao.buscar_por_id.assert_called_once_with(1)
    assert result == produto


def test_atualizar_produto(gateway):
    produto_atualizado = Produto(id=1, nome="Novo", preco=30)

    gateway.dao.atualizar_produto.return_value = produto_atualizado

    result = gateway.atualizar_produto(1, produto_atualizado)

    gateway.dao.atualizar_produto.assert_called_once_with(1, produto_atualizado)
    assert result == produto_atualizado


def test_deletar_produto(gateway):
    gateway.dao.deletar_produto.return_value = None

    result = gateway.deletar_produto(1)

    gateway.dao.deletar_produto.assert_called_once_with(1)
    assert result is None
