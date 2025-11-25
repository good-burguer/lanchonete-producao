from app.infrastructure.api.fastapi import app, Depends

from app.api import check
from app.api import cliente
from app.api import produto

# declare
app.include_router(check.router)
app.include_router(cliente.router)
app.include_router(produto.router)