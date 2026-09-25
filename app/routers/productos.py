from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import ProductoModel
from app.schemas import (
    ProductoCrear,
    ProductoActualizar,
    ProductoRespuesta,
)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
)

# @@@@@@@@@@@@@
# @@ LISTADO @@
# @@@@@@@@@@@@@
@router.get("", response_model=list[ProductoRespuesta])
def listar_productos(
    search: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db)
):
    if search:
        productos = db.query(ProductoModel)\
            .filter(ProductoModel.producto.ilike(f"%{search}%"))\
            .order_by(ProductoModel.producto)\
            .all()
    else:
        productos = db.query(ProductoModel)\
            .order_by(ProductoModel.producto)\
            .all()
            
    return productos


# @@@@@@@@@@@@@@@@@@@@@@@@@
# @@ OBTENER UN PRODUCTO @@
# @@@@@@@@@@@@@@@@@@@@@@@@@
@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto


# @@@@@@@@@@@
# @@ CREAR @@
# @@@@@@@@@@@
@router.post("", response_model=ProductoRespuesta, status_code=201)
def crear_producto(producto: ProductoCrear, db: Session = Depends(get_db)):
    try:
        nuevo_producto = ProductoModel(
            producto=producto.producto,
            precio_venta=producto.precio_venta,
            stock=producto.stock
        )
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto) # Carga el ID autoincremental generado
        return nuevo_producto

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El producto ya existe")


# @@@@@@@@@@@@
# @@ EDITAR @@
# @@@@@@@@@@@@
@router.put("/{producto_id}", response_model=ProductoRespuesta)
def actualizar_producto(
    producto_id: int,
    producto: ProductoActualizar,
    db: Session = Depends(get_db)
):
    existente = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()

    if existente is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    existente.producto = producto.producto
    existente.precio_venta = producto.precio_venta
    existente.stock = producto.stock

    db.commit()
    db.refresh(existente)
    return existente


# @@@@@@@@@@@@@@
# @@ ELIMINAR @@
# @@@@@@@@@@@@@@
@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()
    return None