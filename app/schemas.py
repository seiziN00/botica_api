from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    producto: str = Field(min_length=1)
    precio_venta: float = Field(ge=0)
    stock: int = Field(ge=0)


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(ProductoBase):
    pass


class ProductoRespuesta(ProductoBase):
    id: int