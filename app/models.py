from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class ProductoModel(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    producto = Column(String, index=True, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)