from types import SimpleNamespace
from fastapi.testclient import TestClient
from app.main import app
from app.api.produto import get_produto_gateway
from decimal import Decimal


class MockProdutoGateway:
    def __init__(self):
        categoria = SimpleNamespace(id=1, nome="Lanches")
        self.obj = SimpleNamespace(id=1, nome="X-Burger", descricao="Delicioso", preco=Decimal("12.50"), categoria_rel=categoria)

    def criar_produto(self, produto):
        return self.obj

    def listar_todos(self):
        return [self.obj]

    def listar_por_categoria(self, categoria):
        return [self.obj] if int(categoria) == self.obj.categoria_rel.id else []

    def buscar_por_id(self, id: int):
        return self.obj if id == self.obj.id else None

    def atualizar_produto(self, id: int, produto_data):
        # Accept pydantic models or dicts
        data = None
        if hasattr(produto_data, "model_dump"):
            data = produto_data.model_dump()
        elif hasattr(produto_data, "dict"):
            data = produto_data.dict()
        elif isinstance(produto_data, dict):
            data = produto_data
        else:
            data = {}

        preco_val = data.get("preco", self.obj.preco)
        try:
            preco_decimal = Decimal(str(preco_val))
        except Exception:
            preco_decimal = self.obj.preco

        return SimpleNamespace(id=id, nome=data.get("nome", self.obj.nome), descricao=data.get("descricao", self.obj.descricao), preco=preco_decimal, categoria_rel=self.obj.categoria_rel)

    def deletar_produto(self, id: int):
        return None


def setup_module(module):
    app.dependency_overrides[get_produto_gateway] = lambda: MockProdutoGateway()


def teardown_module(module):
    app.dependency_overrides.clear()


client = TestClient(app)


def test_criar_listar_e_buscar_produto():
    payload = {"nome": "X-Burger", "descricao": "Delicioso", "preco": 12.5, "categoria": 1}

    r = client.post("/produtos/", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "sucess" or body["status"] == "success"
    assert body["data"]["nome"] == "X-Burger"

    r2 = client.get("/produtos/")
    assert r2.status_code == 200
    assert isinstance(r2.json()["data"], list)

    r3 = client.get("/produtos/categoria/1")
    assert r3.status_code == 200
    assert len(r3.json()["data"]) >= 1

    r4 = client.get("/produtos/1")
    assert r4.status_code == 200
    assert r4.json()["data"]["id"] == 1


def test_atualizar_e_deletar_produto():
    update_payload = {"nome": "X-Burger Mega", "preco": 15.0}
    r = client.put("/produtos/1", json=update_payload)
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["nome"] == "X-Burger Mega"

    r2 = client.delete("/produtos/1")
    assert r2.status_code == 204
