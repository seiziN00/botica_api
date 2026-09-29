from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class ProductoModel(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    producto = Column(String, index=True, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)