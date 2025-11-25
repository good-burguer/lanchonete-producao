from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.entities.produto.entities import ProdutoEntities
from app.entities.produto.models import Produto
from app.adapters.enums.categoria_produto import CategoriaProdutoEnum
from app.models.produto import Produto
from app.dao.produto_dao import ProdutoDAO

class ProdutoGateway(ProdutoEntities):
    def __init__(self, db_session: Session):
        self.dao = ProdutoDAO(db_session)

    def criar_produto(self, produto: Produto) -> Produto:
        
        return self.dao.criar_produto(produto)

    def listar_todos(self) -> list[Produto]:
        
        return self.dao.listar_todos()
    
    def listar_por_categoria(self, categoria: CategoriaProdutoEnum) -> list[Produto]:
        
        return self.dao.listar_por_categoria(categoria)
    
    def buscar_por_id(self, id: int) -> Produto:
       
       return self.dao.buscar_por_id(id)

    def atualizar_produto(self, id: int, produto_data: Produto) -> Produto:
        
        return self.dao.atualizar_produto(id, produto_data)
    
    def deletar_produto(self, id: int) -> None :
        
        return self.dao.deletar_produto(id)
    