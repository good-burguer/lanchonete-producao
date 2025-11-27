import pytest
from unittest.mock import Mock, MagicMock
from decimal import Decimal

from app.use_cases.produto_use_case import ProdutoUseCase
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.adapters.schemas.categoria_produto import CategoriaProdutoResponseSchema


@pytest.fixture
def mock_entity():

    return Mock()


@pytest.fixture
def use_case(mock_entity):
    
    return ProdutoUseCase(entity=mock_entity)


@pytest.fixture
def mock_produto_model():
    produto = Mock()
    produto.id = 5
    produto.nome = "Hamburguer"
    produto.descricao = "Pão, carne e queijo"
    produto.preco = Decimal("1.00")
    
    # Mock da categoria relacionada
    categoria = Mock()
    categoria.id = 1
    categoria.nome = "Lanche"
    produto.categoria_rel = categoria
    
    return produto


@pytest.fixture
def mock_produtos_list():
    produtos = []
    
    # Produto 1 - Lanche
    produto1 = Mock()
    produto1.id = 1
    produto1.nome = "X-Burger"
    produto1.descricao = "Hambúrguer com queijo"
    produto1.preco = Decimal("25.90")
    categoria1 = Mock()
    categoria1.id = 1
    categoria1.nome = "Lanche"
    produto1.categoria_rel = categoria1
    produtos.append(produto1)
    
    # Produto 2 - Bebida
    produto2 = Mock()
    produto2.id = 2
    produto2.nome = "Refrigerante"
    produto2.descricao = "Coca-Cola 350ml"
    produto2.preco = Decimal("5.00")
    categoria2 = Mock()
    categoria2.id = 2
    categoria2.nome = "Bebida"
    produto2.categoria_rel = categoria2
    produtos.append(produto2)
    
    return produtos


@pytest.fixture
def sample_produto_create_dto():
    return {
        "nome": "Hamburguer",
        "descricao": "Pão, carne e queijo",
        "categoria": 1,
        "preco": Decimal("1.00")
    }


class TestCriarProduto:
    
    def test_criar_produto_sucesso(self, use_case, mock_entity, mock_produto_model,
                                   sample_produto_create_dto):

        # Arrange
        mock_entity.criar_produto.return_value = mock_produto_model
        
        # Act
        result = use_case.criar_produto(sample_produto_create_dto)
        
        # Assert
        mock_entity.criar_produto.assert_called_once_with(sample_produto_create_dto)
        assert isinstance(result, ProdutoResponseSchema)
        assert result.id == 5
        assert result.nome == "Hamburguer"
        assert result.preco == Decimal("1.00")
        assert result.categoria.id == 1
        assert result.categoria.nome == "Lanche"
    
    def test_criar_produto_retorna_schema_correto(self, use_case, mock_entity, mock_produto_model,
                                                  sample_produto_create_dto):

        # Arrange
        mock_entity.criar_produto.return_value = mock_produto_model
        
        # Act
        result = use_case.criar_produto(sample_produto_create_dto)
        
        # Assert
        assert hasattr(result, 'id')
        assert hasattr(result, 'nome')
        assert hasattr(result, 'descricao')
        assert hasattr(result, 'preco')
        assert hasattr(result, 'categoria')
        assert isinstance(result.categoria, CategoriaProdutoResponseSchema)


class TestListarTodos:
    
    def test_listar_todos_sucesso(self, use_case, mock_entity, mock_produtos_list):

        # Arrange
        mock_entity.listar_todos.return_value = mock_produtos_list
        
        # Act
        result = use_case.listar_todos()
        
        # Assert
        mock_entity.listar_todos.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(p, ProdutoResponseSchema) for p in result)
        assert result[0].nome == "X-Burger"
        assert result[1].nome == "Refrigerante"
        assert result[0].categoria.nome == "Lanche"
        assert result[1].categoria.nome == "Bebida"
    
    def test_listar_todos_vazio(self, use_case, mock_entity):

        # Arrange
        mock_entity.listar_todos.return_value = []
        
        # Act
        result = use_case.listar_todos()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_listar_todos_converte_todos_produtos_para_schema(self, use_case, mock_entity,
                                                              mock_produtos_list):

        # Arrange
        mock_entity.listar_todos.return_value = mock_produtos_list
        
        # Act
        result = use_case.listar_todos()
        
        # Assert
        for produto in result:
            assert isinstance(produto, ProdutoResponseSchema)
            assert isinstance(produto.categoria, CategoriaProdutoResponseSchema)


class TestListarPorCategoria:
    
    def test_listar_por_categoria_sucesso(self, use_case, mock_entity):

        # Arrange
        produto_lanche = Mock()
        produto_lanche.id = 1
        produto_lanche.nome = "X-Burger"
        produto_lanche.descricao = "Hambúrguer com queijo"
        produto_lanche.preco = Decimal("25.90")
        categoria = Mock()
        categoria.id = 1
        categoria.nome = "Lanche"
        produto_lanche.categoria_rel = categoria
        
        mock_entity.listar_por_categoria.return_value = [produto_lanche]
        
        # Act
        result = use_case.listar_por_categoria(1)
        
        # Assert
        mock_entity.listar_por_categoria.assert_called_once_with(1)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProdutoResponseSchema)
        assert result[0].categoria.id == 1
        assert result[0].categoria.nome == "Lanche"
    
    def test_listar_por_categoria_vazia(self, use_case, mock_entity):

        # Arrange
        mock_entity.listar_por_categoria.return_value = []
        
        # Act
        result = use_case.listar_por_categoria(4)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_listar_por_categoria_multiplos_produtos(self, use_case, mock_entity):

        # Arrange
        produtos_bebida = []
        for i in range(1, 4):
            produto = Mock()
            produto.id = i
            produto.nome = f"Bebida {i}"
            produto.descricao = f"Descrição {i}"
            produto.preco = Decimal(f"{i}.00")
            categoria = Mock()
            categoria.id = 2
            categoria.nome = "Bebida"
            produto.categoria_rel = categoria
            produtos_bebida.append(produto)
        
        mock_entity.listar_por_categoria.return_value = produtos_bebida
        
        # Act
        result = use_case.listar_por_categoria(2)
        
        # Assert
        assert len(result) == 3
        assert all(p.categoria.nome == "Bebida" for p in result)


class TestBuscarPorId:
    
    def test_buscar_por_id_sucesso(self, use_case, mock_entity, mock_produto_model):

        # Arrange
        mock_entity.buscar_por_id.return_value = mock_produto_model
        
        # Act
        result = use_case.buscar_por_id(5)
        
        # Assert
        mock_entity.buscar_por_id.assert_called_once_with(5)
        assert isinstance(result, ProdutoResponseSchema)
        assert result.id == 5
        assert result.nome == "Hamburguer"
    
    def test_buscar_por_id_nao_encontrado(self, use_case, mock_entity):

        # Arrange
        mock_entity.buscar_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            use_case.buscar_por_id(999)
        
        assert "Produto não encontrado" in str(exc_info.value)
    
    def test_buscar_por_id_retorna_schema_completo(self, use_case, mock_entity, mock_produto_model):

        # Arrange
        mock_entity.buscar_por_id.return_value = mock_produto_model
        
        # Act
        result = use_case.buscar_por_id(5)
        
        # Assert
        assert result.id == 5
        assert result.categoria.id == 1
        assert result.categoria.nome == "Lanche"


class TestAtualizarProduto:
    
    def test_atualizar_produto_sucesso(self, use_case, mock_entity, mock_produto_model):

        # Arrange
        update_data = {
            "nome": "Hamburguer Premium",
            "preco": Decimal("15.00")
        }
        
        # Atualiza o mock para refletir as mudanças
        mock_produto_model.nome = "Hamburguer Premium"
        mock_produto_model.preco = Decimal("15.00")
        
        mock_entity.atualizar_produto.return_value = mock_produto_model
        
        # Act
        result = use_case.atualizar_produto(5, update_data)
        
        # Assert
        mock_entity.atualizar_produto.assert_called_once_with(5, update_data)
        assert isinstance(result, ProdutoResponseSchema)
        assert result.id == 5
        assert result.nome == "Hamburguer Premium"
        assert result.preco == Decimal("15.00")
    
    def test_atualizar_produto_nao_encontrado(self, use_case, mock_entity):

        # Arrange
        update_data = {"preco": Decimal("20.00")}
        mock_entity.atualizar_produto.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            use_case.atualizar_produto(999, update_data)
        
        assert "Produto não encontrado" in str(exc_info.value)
    
    def test_atualizar_produto_retorna_schema_atualizado(self, use_case, mock_entity,
                                                         mock_produto_model):

        # Arrange
        update_data = {"descricao": "Nova descrição"}
        mock_produto_model.descricao = "Nova descrição"
        mock_entity.atualizar_produto.return_value = mock_produto_model
        
        # Act
        result = use_case.atualizar_produto(5, update_data)
        
        # Assert
        assert result.descricao == "Nova descrição"
        assert isinstance(result.categoria, CategoriaProdutoResponseSchema)


class TestDeletarProduto:
    
    def test_deletar_produto_sucesso(self, use_case, mock_entity):

        # Arrange
        mock_entity.deletar_produto.return_value = None
        
        # Act
        result = use_case.deletar_produto(5)
        
        # Assert
        mock_entity.deletar_produto.assert_called_once_with(5)
        assert result is None
    
    def test_deletar_produto_chama_entity(self, use_case, mock_entity):

        # Arrange
        produto_id = 10
        mock_entity.deletar_produto.return_value = None
        
        # Act
        use_case.deletar_produto(produto_id)
        
        # Assert
        mock_entity.deletar_produto.assert_called_once_with(produto_id)


class TestCreateResponseSchema:
    
    def test_create_response_schema_converte_corretamente(self, use_case, mock_produto_model):

        # Act
        result = use_case._create_response_schema(mock_produto_model)
        
        # Assert
        assert isinstance(result, ProdutoResponseSchema)
        assert result.id == mock_produto_model.id
        assert result.nome == mock_produto_model.nome
        assert result.descricao == mock_produto_model.descricao
        assert result.preco == mock_produto_model.preco
        assert isinstance(result.categoria, CategoriaProdutoResponseSchema)
        assert result.categoria.id == mock_produto_model.categoria_rel.id
        assert result.categoria.nome == mock_produto_model.categoria_rel.nome
    
    def test_create_response_schema_preserva_tipos(self, use_case, mock_produto_model):

        # Act
        result = use_case._create_response_schema(mock_produto_model)
        
        # Assert
        assert isinstance(result.id, int)
        assert isinstance(result.nome, str)
        assert isinstance(result.preco, Decimal)
        assert isinstance(result.categoria.id, int)
        assert isinstance(result.categoria.nome, str)


class TestProdutoUseCaseIntegration:
    
    def test_use_case_inicializacao(self, mock_entity):

        # Act
        use_case = ProdutoUseCase(entity=mock_entity)
        
        # Assert
        assert use_case.produto_entity == mock_entity
        assert isinstance(use_case, ProdutoUseCase)
    
    def test_fluxo_completo_crud(self, use_case, mock_entity):

        # Arrange - Create
        produto_novo = Mock()
        produto_novo.id = 1
        produto_novo.nome = "Produto Teste"
        produto_novo.descricao = "Descrição teste"
        produto_novo.preco = Decimal("10.00")
        categoria = Mock()
        categoria.id = 1
        categoria.nome = "Lanche"
        produto_novo.categoria_rel = categoria
        
        mock_entity.criar_produto.return_value = produto_novo
        mock_entity.buscar_por_id.return_value = produto_novo
        mock_entity.listar_todos.return_value = [produto_novo]
        
        # Create
        result_create = use_case.criar_produto({"nome": "Produto Teste"})
        assert result_create.nome == "Produto Teste"
        
        # Read
        result_read = use_case.buscar_por_id(1)
        assert result_read.id == 1
        
        # List
        result_list = use_case.listar_todos()
        assert len(result_list) == 1
        
        # Update
        produto_novo.nome = "Produto Atualizado"
        mock_entity.atualizar_produto.return_value = produto_novo
        result_update = use_case.atualizar_produto(1, {"nome": "Produto Atualizado"})
        assert result_update.nome == "Produto Atualizado"
        
        # Delete
        mock_entity.deletar_produto.return_value = None
        result_delete = use_case.deletar_produto(1)
        assert result_delete is None