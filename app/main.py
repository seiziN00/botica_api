from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import productos

# Crear las tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Farmacia",
    description="API para gestionar el catálogo de productos",
    version="1.0.0",
)

app.include_router(productos.router)

@app.get("/")
def root():
    return {
        "mensaje": "API Farmacia funcionando"
    }