from pydantic import BaseModel, Field, EmailStr


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



# Para el Login
class UsuarioLogin(BaseModel):
    email: str
    password: str

# Para crear un usuario (manualmente por ahora)
class UsuarioCrear(BaseModel):
    nombre: str
    email: str
    password: str

# Respuesta segura (sin password)
class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str
    
    class Config:
        from_attributes = True