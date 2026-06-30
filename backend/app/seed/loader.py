import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import (
    Provincia, Municipio, Producto, AlmacenCentral, 
    PuntoVenta, Inventario, EntradaMercancia,
    Asignacion, Merma, PerdidaTransporte
)
import os


def cargar_provincias(session: Session, filepath: str):
    print("Cargando provincias...")
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        provincia = Provincia(
            id=int(row["id"]),
            nombre=row["nombre"],
            codigo=row["codigo"]
        )
        session.merge(provincia)
    session.commit()
    print(f"  {len(df)} provincias cargadas")


def cargar_municipios(session: Session, filepath: str):
    print("Cargando municipios...")
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        municipio = Municipio(
            id=int(row["id"]),
            nombre=row["nombre"],
            provincia_id=int(row["provincia_id"]),
            poblacion=int(row["poblacion"])
        )
        session.merge(municipio)
    session.commit()
    print(f"  {len(df)} municipios cargados")


def cargar_productos(session: Session, filepath: str):
    print("Cargando productos...")
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        producto = Producto(
            id=int(row["id"]),
            nombre=row["nombre"],
            categoria=row["categoria"],
            unidad_medida=row["unidad_medida"],
            vida_util_dias=int(row["vida_util_dias"])
        )
        session.merge(producto)
    session.commit()
    print(f"  {len(df)} productos cargados")


def cargar_almacenes(session: Session):
    print("Cargando almacenes centrales...")
    provincias = session.query(Provincia).all()
    for idx, provincia in enumerate(provincias, 1):
        almacen = AlmacenCentral(
            id=idx,
            nombre=f"Almacén Central {provincia.nombre}",
            provincia_id=provincia.id,
            capacidad_max=100000.0
        )
        session.merge(almacen)
    session.commit()
    print(f"  {len(provincias)} almacenes centrales creados")


def cargar_puntos_venta(session: Session):
    print("Cargando puntos de venta...")
    municipios = session.query(Municipio).all()
    pv_id = 1
    for municipio in municipios:
        num_bodegas = max(3, municipio.poblacion // 20000)
        for i in range(num_bodegas):
            pv = PuntoVenta(
                id=pv_id,
                nombre=f"Bodega {municipio.nombre} #{i+1}",
                tipo="bodega",
                municipio_id=municipio.id,
                capacidad_max=5000.0
            )
            session.merge(pv)
            pv_id += 1
    session.commit()
    print(f"  {pv_id - 1} puntos de venta creados")


def cargar_inventarios(session: Session, filepath: str):
    print("Cargando inventarios...")
    df = pd.read_csv(filepath)
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    batch_size = 10000
    total = len(df)
    
    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        rows = []
        for _, row in batch.iterrows():
            rows.append({
                "id": int(row["id"]),
                "producto_id": int(row["producto_id"]),
                "punto_venta_id": int(row["punto_venta_id"]),
                "fecha": row["fecha"],
                "cantidad": float(row["cantidad"]),
            })
        session.execute(Inventario.__table__.insert(), rows)
        session.commit()
        print(f"  Procesados {min(start + batch_size, total)}/{total} registros")
    print(f"  {total} inventarios cargados")


def cargar_entradas(session: Session, filepath: str):
    print("Cargando entradas de mercancía...")
    df = pd.read_csv(filepath)
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    batch_size = 10000
    total = len(df)
    
    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        rows = []
        for _, row in batch.iterrows():
            rows.append({
                "producto_id": int(row["producto_id"]),
                "punto_venta_id": int(row["punto_venta_id"]),
                "fecha": row["fecha"],
                "cantidad": float(row["cantidad"]),
                "proveedor": row["proveedor"],
            })
        session.execute(EntradaMercancia.__table__.insert(), rows)
        session.commit()
        print(f"  Procesados {min(start + batch_size, total)}/{total} registros")
    print(f"  {total} entradas cargadas")


def cargar_asignaciones(session: Session, filepath: str):
    print("Cargando asignaciones...")
    df = pd.read_csv(filepath)
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    batch_size = 10000
    total = len(df)
    
    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        rows = []
        for _, row in batch.iterrows():
            rows.append({
                "id": int(row["id"]),
                "producto_id": int(row["producto_id"]),
                "almacen_origen_id": int(row["almacen_origen_id"]),
                "punto_venta_destino_id": int(row["punto_venta_destino_id"]),
                "fecha": row["fecha"],
                "cantidad": float(row["cantidad"]),
                "estado": row["estado"],
            })
        session.execute(Asignacion.__table__.insert(), rows)
        session.commit()
        print(f"  Procesados {min(start + batch_size, total)}/{total} registros")
    print(f"  {total} asignaciones cargadas")


def cargar_mermas(session: Session, filepath: str):
    print("Cargando mermas...")
    df = pd.read_csv(filepath)
    df["fecha"] = pd.to_datetime(df["fecha"])
    batch_size = 10000
    total = len(df)
    
    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        rows = []
        for _, row in batch.iterrows():
            rows.append({
                "inventario_id": int(row["inventario_id"]),
                "cantidad": float(row["cantidad"]),
                "motivo": row["motivo"],
                "fecha": row["fecha"],
            })
        session.execute(Merma.__table__.insert(), rows)
        session.commit()
        print(f"  Procesados {min(start + batch_size, total)}/{total} registros")
    print(f"  {total} mermas cargadas")


def cargar_perdidas(session: Session, filepath: str):
    print("Cargando pérdidas de transporte...")
    df = pd.read_csv(filepath)
    df["fecha"] = pd.to_datetime(df["fecha"])
    batch_size = 10000
    total = len(df)
    
    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        rows = []
        for _, row in batch.iterrows():
            rows.append({
                "asignacion_id": int(row["asignacion_id"]),
                "cantidad": float(row["cantidad"]),
                "motivo": row["motivo"],
                "fecha": row["fecha"],
            })
        session.execute(PerdidaTransporte.__table__.insert(), rows)
        session.commit()
        print(f"  Procesados {min(start + batch_size, total)}/{total} registros")
    print(f"  {total} pérdidas de transporte cargadas")


def cargar_datos_completos(seeds_dir: str = "database/seeds"):
    print("=" * 60)
    print("ALIMENDATA - Carga de datos iniciales")
    print("=" * 60)
    print("NOTA: Las tablas deben existir previamente (ejecutar: alembic upgrade head)")
    print("=" * 60)
    
    session = SessionLocal()
    
    try:
        cargar_provincias(session, os.path.join(seeds_dir, "provincias.csv"))
        cargar_municipios(session, os.path.join(seeds_dir, "municipios.csv"))
        cargar_productos(session, os.path.join(seeds_dir, "productos.csv"))
        cargar_almacenes(session)
        cargar_puntos_venta(session)
        cargar_inventarios(session, os.path.join(seeds_dir, "inventarios.csv"))
        cargar_entradas(session, os.path.join(seeds_dir, "entradas.csv"))
        cargar_asignaciones(session, os.path.join(seeds_dir, "asignaciones.csv"))
        cargar_mermas(session, os.path.join(seeds_dir, "mermas.csv"))
        cargar_perdidas(session, os.path.join(seeds_dir, "perdidas_transporte.csv"))
        
        print("=" * 60)
        print("CARGA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error durante la carga: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    cargar_datos_completos()
