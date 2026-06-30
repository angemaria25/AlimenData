import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from app.models.models import Inventario, Producto, PuntoVenta, Municipio, Provincia, EntradaMercancia
import os


def generar_mapa_calor_inventarios(
    session: Session,
    producto_id: int,
    anio: int,
    output_dir: str = "database/seeds"
):
    datos = session.query(
        Municipio.nombre,
        extract('month', Inventario.fecha).label('mes'),
        func.sum(Inventario.cantidad).label("total")
    ).join(
        PuntoVenta, PuntoVenta.municipio_id == Municipio.id
    ).join(
        Inventario, Inventario.punto_venta_id == PuntoVenta.id
    ).filter(
        and_(
            Inventario.producto_id == producto_id,
            extract('year', Inventario.fecha) == anio
        )
    ).group_by(
        Municipio.nombre, extract('month', Inventario.fecha)
    ).all()

    if not datos:
        print("No hay datos para generar el mapa de calor")
        return None

    df = pd.DataFrame(datos, columns=["municipio", "mes", "total"])
    pivot = df.pivot(index="municipio", columns="mes", values="total")

    plt.figure(figsize=(14, 10))
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": "Cantidad en inventario"}
    )
    plt.title(f"Mapa de Calor - Inventario por Municipio y Mes ({anio})", fontsize=14)
    plt.xlabel("Mes", fontsize=12)
    plt.ylabel("Municipio", fontsize=12)
    plt.tight_layout()

    producto = session.query(Producto).filter(Producto.id == producto_id).first()
    nombre_producto = producto.nombre if producto else "producto"

    filepath = os.path.join(output_dir, f"mapa_calor_{nombre_producto}_{anio}.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Mapa de calor guardado en: {filepath}")
    return filepath


def generar_mapa_calor_estado_critico(
    session: Session,
    producto_id: int,
    anio: int,
    umbral_critico: int = 7,
    umbral_alerta: int = 15,
    output_dir: str = "database/seeds"
):
    meses = list(range(1, 13))
    nombres_meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                     "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    municipios = session.query(Municipio).all()

    matriz_estado = []
    nombres_municipios = []

    for municipio in municipios:
        fila_estado = []
        for mes in meses:
            promedio_stock = session.query(
                func.avg(Inventario.cantidad)
            ).join(PuntoVenta).filter(
                and_(
                    Inventario.producto_id == producto_id,
                    PuntoVenta.municipio_id == municipio.id,
                    extract('month', Inventario.fecha) == mes,
                    extract('year', Inventario.fecha) == anio
                )
            ).scalar() or 0

            promedio_entradas = session.query(
                func.coalesce(func.avg(EntradaMercancia.cantidad), 0)
            ).join(PuntoVenta).filter(
                and_(
                    EntradaMercancia.producto_id == producto_id,
                    PuntoVenta.municipio_id == municipio.id,
                    extract('month', EntradaMercancia.fecha) == mes,
                    extract('year', EntradaMercancia.fecha) == anio
                )
            ).scalar() or 0

            if promedio_entradas > 0:
                dias_stock = promedio_stock / (promedio_entradas / 30)
            else:
                dias_stock = 30

            if dias_stock < umbral_critico:
                estado_num = 0
            elif dias_stock < umbral_alerta:
                estado_num = 1
            elif dias_stock < 30:
                estado_num = 2
            else:
                estado_num = 3

            fila_estado.append(estado_num)

        matriz_estado.append(fila_estado)
        nombres_municipios.append(municipio.nombre)

    if not matriz_estado:
        print("No hay datos para generar el mapa de calor de estado crítico")
        return None

    df = pd.DataFrame(matriz_estado, index=nombres_municipios, columns=nombres_meses)

    cmap = plt.cm.colors.ListedColormap(['#d32f2f', '#ff9800', '#fdd835', '#4caf50'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(14, 10))
    im = ax.imshow(df.values, cmap=cmap, norm=norm, aspect='auto')

    ax.set_xticks(range(len(nombres_meses)))
    ax.set_xticklabels(nombres_meses)
    ax.set_yticks(range(len(nombres_municipios)))
    ax.set_yticklabels(nombres_municipios)

    for i in range(len(nombres_municipios)):
        for j in range(len(nombres_meses)):
            ax.text(j, i, str(round(df.values[i, j], 1)),
                   ha="center", va="center", fontsize=7,
                   color="white" if df.values[i, j] < 1.5 else "black")

    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
    cbar.set_ticklabels(["Critico (<7d)", "Alerta (<15d)", "Normal (<30d)", "Suficiente (>30d)"])
    cbar.set_label("Nivel de Stock", fontsize=12)

    producto = session.query(Producto).filter(Producto.id == producto_id).first()
    nombre_producto = producto.nombre if producto else "producto"

    plt.title(f"Estado Critico de Inventario - {nombre_producto.title()} ({anio})", fontsize=14)
    plt.xlabel("Mes", fontsize=12)
    plt.ylabel("Municipio", fontsize=12)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f"estado_critico_{nombre_producto}_{anio}.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Mapa de calor de estado critico guardado en: {filepath}")
    return filepath


def generar_grafico_tendencia_producto(
    session: Session,
    producto_id: int,
    municipio_id: int,
    output_dir: str = "database/seeds"
):
    datos = session.query(
        Inventario.fecha,
        func.sum(Inventario.cantidad).label("total")
    ).join(
        PuntoVenta, PuntoVenta.id == Inventario.punto_venta_id
    ).filter(
        and_(
            Inventario.producto_id == producto_id,
            PuntoVenta.municipio_id == municipio_id
        )
    ).group_by(
        Inventario.fecha
    ).order_by(
        Inventario.fecha
    ).all()

    if not datos:
        print("No hay datos para generar el grafico de tendencia")
        return None

    df = pd.DataFrame(datos, columns=["fecha", "total"])
    df["fecha"] = pd.to_datetime(df["fecha"])

    plt.figure(figsize=(16, 6))
    plt.plot(df["fecha"], df["total"], marker="o", markersize=3, linewidth=1.5)
    plt.title(f"Tendencia de Inventario - Producto {producto_id} en Municipio {municipio_id}", fontsize=14)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Cantidad Total", fontsize=12)
    plt.xticks(rotation=45, fontsize=8)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f"tendencia_p{producto_id}_m{municipio_id}.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Grafico de tendencia guardado en: {filepath}")
    return filepath


def generar_resumen_visual(
    session: Session,
    output_dir: str = "database/seeds"
):
    os.makedirs(output_dir, exist_ok=True)

    productos = session.query(Producto).all()

    ultimo_anio = session.query(func.max(func.extract('year', Inventario.fecha))).scalar()
    anio_actual = int(ultimo_anio) if ultimo_anio else datetime.now().year

    for producto in productos:
        generar_mapa_calor_inventarios(session, producto.id, anio_actual, output_dir)
        generar_mapa_calor_estado_critico(session, producto.id, anio_actual, output_dir=output_dir)

    primer_producto = session.query(Producto).first()
    primer_municipio = session.query(PuntoVenta).first()
    if primer_producto and primer_municipio:
        generar_grafico_tendencia_producto(session, primer_producto.id, primer_municipio.id, output_dir)

    print("Resumen visual generado exitosamente")


if __name__ == "__main__":
    from app.database import SessionLocal
    session = SessionLocal()
    try:
        print("=" * 60)
        print("ALIMENDATA - GENERACIÓN DE VISUALIZACIONES")
        print("=" * 60)
        generar_resumen_visual(session)
        print("\nVisualizaciones generadas exitosamente.")
    finally:
        session.close()
