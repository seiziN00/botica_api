import csv
from pathlib import Path
from app.database import SessionLocal, engine
from app.models import Base, ProductoModel

CSV_FILE = Path("productos.csv")


def importar_productos():
    # Verificar que las tablas existan
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Esto es para evitar duplicados por si se ejecuta dos veces
        if db.query(ProductoModel).count() > 0:
            print("⚠️ La base de datos ya contiene productos. No se realizó la importación masiva.")
            return

        if not CSV_FILE.exists():
            print(f"❌ No se encontró el archivo {CSV_FILE}")
            return

        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as archivo:
            reader = csv.DictReader(archivo, delimiter=",")
            productos_a_insertar = []

            for fila in reader:
                nombre = fila["PRODUCTO FORMATEADO"].strip()
                
                precio = float(
                    fila["P. VENTA"]
                    .strip()
                    .replace(",", ".")
                )
                
                stock = int(
                    fila["TOTAL/ STOCK"].strip()
                )

                producto_obj = ProductoModel(
                    producto=nombre,
                    precio_venta=precio,
                    stock=stock
                )
                productos_a_insertar.append(producto_obj)

            db.add_all(productos_a_insertar)
            db.commit()
            print(f"✅ Importación completada: {len(productos_a_insertar)} productos guardados con éxito.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la importación: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    importar_productos()