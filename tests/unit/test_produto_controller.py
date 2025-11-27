import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException, status
from decimal import Decimal

from app.controllers.produto_controller import ProdutoController
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.adapters.schemas.categoria_produto import CategoriaProdutoResponseSchema


@pytest.fixture
def mock_gateway():
    
    return Mock()


@pytest.fixture
def controller(mock_gateway):
    
    return ProdutoController(db_session=mock_gateway)


@pytest.fixture
def sample_categoria_schema():
    
    return CategoriaProdutoResponseSchema(
        id=1,
        nome="Lanche"
    )


@pytest.fixture
def sample_produto_response_schema(sample_categoria_schema):
    
    return ProdutoResponseSchema(
        id=5,
        nome="Hamburguer",
        descricao="Pão, carne e queijo",
        preco=Decimal("1.00"),
        categoria=sample_categoria_schema
    )


@pytest.fixture
def sample_produto_create_dto():
    
    return {
        "nome": "Hamburguer",
        "descricao": "Pão, carne e queijo",
        "categoria": 1,
        "preco": Decimal("1.00")
    }


class TestCriarProduto:
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_criar_produto_sucesso(self, mock_use_case, controller, mock_gateway,
                                   sample_produto_create_dto, sample_produto_response_schema):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.criar_produto.return_value = sample_produto_response_schema
        
        # Act
        result = controller.criar_produto(sample_produto_create_dto)
        
        # Assert
        mock_use_case.assert_called_once_with(mock_gateway)
        mock_use_case_instance.criar_produto.assert_called_once_with(sample_produto_create_dto)
        assert result.status == 'sucess'
        assert result.data.id == 5
        assert result.data.nome == 'Hamburguer'
        assert result.data.categoria.id == 1
        assert result.data.categoria.nome == 'Lanche'
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_criar_produto_erro_generico(self, mock_use_case, controller, sample_produto_create_dto):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.criar_produto.side_effect = Exception("Erro ao criar produto")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.criar_produto(sample_produto_create_dto)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Erro ao criar produto" in str(exc_info.value.detail)


class TestListarTodos:
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_listar_todos_sucesso(self, mock_use_case, controller, mock_gateway):

        # Arrange
        produtos_mock = [
            ProdutoResponseSchema(
                id=1,
                nome="X-Burger",
                descricao="Hambúrguer com queijo",
                preco=Decimal("25.90"),
                categoria=CategoriaProdutoResponseSchema(id=1, nome="Lanche")
            ),
            ProdutoResponseSchema(
                id=2,
                nome="Refrigerante",
                descricao="Coca-Cola 350ml",
                preco=Decimal("5.00"),
                categoria=CategoriaProdutoResponseSchema(id=2, nome="Bebida")
            )
        ]
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.listar_todos.return_value = produtos_mock
        
        # Act
        result = controller.listar_todos()
        
        # Assert
        mock_use_case.assert_called_once_with(mock_gateway)
        mock_use_case_instance.listar_todos.assert_called_once()
        assert result.status == 'sucess'
        assert len(result.data) == 2
        assert result.data[0].nome == "X-Burger"
        assert result.data[1].categoria.nome == "Bebida"
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_listar_todos_vazio(self, mock_use_case, controller, mock_gateway):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.listar_todos.return_value = []
        
        # Act
        result = controller.listar_todos()
        
        # Assert
        assert result.status == 'sucess'
        assert len(result.data) == 0
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_listar_todos_erro(self, mock_use_case, controller):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.listar_todos.side_effect = Exception("Erro no banco")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.listar_todos()
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


class TestListarProdutosPorCategoria:
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_listar_por_categoria_sucesso(self, mock_use_case, controller, mock_gateway):

        # Arrange
        lanches = [
            ProdutoResponseSchema(
                id=1,
                nome="X-Burger",
                descricao="Hambúrguer com queijo",
                preco=Decimal("25.90"),
                categoria=CategoriaProdutoResponseSchema(id=1, nome="Lanche")
            )
        ]
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.listar_por_categoria.return_value = lanches
        
        # Act
        result = controller.listar_produtos_por_categoria(1)
        
        # Assert
        mock_use_case.assert_called_once_with(mock_gateway)
        mock_use_case_instance.listar_por_categoria.assert_called_once_with(1)
        assert result.status == 'sucess'
        assert len(result.data) == 1
        assert result.data[0].categoria.id == 1
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_listar_por_categoria_erro(self, mock_use_case, controller):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.listar_por_categoria.side_effect = Exception("Categoria inválida")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.listar_produtos_por_categoria(999)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


class TestBuscarProduto:
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_buscar_produto_sucesso(self, mock_use_case, controller, mock_gateway,
                                    sample_produto_response_schema):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.buscar_por_id.return_value = sample_produto_response_schema
        
        # Act
        result = controller.buscar_produto(5)
        
        # Assert
        mock_use_case.assert_called_once_with(mock_gateway)
        mock_use_case_instance.buscar_por_id.assert_called_once_with(5)
        assert result.status == 'sucess'
        assert result.data.id == 5
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_buscar_produto_nao_encontrado(self, mock_use_case, controller):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.buscar_por_id.side_effect = ValueError("Produto não encontrado")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_produto(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_buscar_produto_erro_generico(self, mock_use_case, controller):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.buscar_por_id.side_effect = Exception("Erro no banco")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_produto(1)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


class TestAtualizarProduto:
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_atualizar_produto_sucesso(self, mock_use_case, controller, mock_gateway):

        # Arrange
        update_data = {"nome": "Hamburguer Premium", "preco": Decimal("15.00")}
        updated_schema = ProdutoResponseSchema(
            id=5,
            nome="Hamburguer Premium",
            descricao="Pão, carne e queijo",
            preco=Decimal("15.00"),
            categoria=CategoriaProdutoResponseSchema(id=1, nome="Lanche")
        )
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.atualizar_produto.return_value = updated_schema
        
        # Act
        result = controller.atualizar_produto(5, update_data)
        
        # Assert
        mock_use_case.assert_called_once_with(mock_gateway)
        mock_use_case_instance.atualizar_produto.assert_called_once_with(5, produto_data=update_data)
        assert result.status == 'sucess'
        assert result.data.nome == "Hamburguer Premium"
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_atualizar_produto_nao_encontrado(self, mock_use_case, controller):

        # Arrange
        update_data = {"preco": Decimal("20.00")}
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.atualizar_produto.side_effect = ValueError("Produto não encontrado")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_produto(999, update_data)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_atualizar_produto_erro_generico(self, mock_use_case, controller):

        # Arrange
        update_data = {"preco": Decimal("-10.00")}
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.atualizar_produto.side_effect = Exception("Preço inválido")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_produto(5, update_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


class TestDeletarProduto:
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_deletar_produto_sucesso(self, mock_use_case, controller, mock_gateway):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.deletar_produto.return_value = None
        
        # Act
        result = controller.deletar_produto(5)
        
        # Assert
        mock_use_case.assert_called_once_with(mock_gateway)
        mock_use_case_instance.deletar_produto.assert_called_once_with(5)
        assert result.status_code == status.HTTP_204_NO_CONTENT
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_deletar_produto_nao_encontrado(self, mock_use_case, controller):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.deletar_produto.side_effect = ValueError("Produto não encontrado")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.deletar_produto(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.controllers.produto_controller.ProdutoUseCase')
    def test_deletar_produto_erro_generico(self, mock_use_case, controller):

        # Arrange
        mock_use_case_instance = mock_use_case.return_value
        mock_use_case_instance.deletar_produto.side_effect = Exception("Erro ao deletar")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            controller.deletar_produto(5)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


class TestProdutoControllerIntegration:
    
    def test_controller_inicializacao(self, mock_gateway):

        # Act
        controller = ProdutoController(db_session=mock_gateway)
        
        # Assert
        assert controller.db_session == mock_gateway
        assert isinstance(controller, ProdutoController)