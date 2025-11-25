from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.db.database import Base
from app.models.categoria_produto import CategoriaProduto

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
    imagem = Column(String(255), nullable=True)
    categoria = Column(Integer, ForeignKey("categoria_produto.id"), nullable=False)

    categoria_rel = relationship("CategoriaProduto")