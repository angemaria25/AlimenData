from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from app.models.models import Inventario, Producto, PuntoVenta, Municipio, Provincia, EntradaMercancia
from typing import List, Dict, Optional
from datetime import datetime, date


def calcular_velocidad_rotacion(
    session: Session,
    producto_id: int,
    punto_venta_id: int,
    fecha: date
) -> float:
    inventario = session.query(Inventario).filter(
        and_(
            Inventario.producto_id == producto_id,
            Inventario.punto_venta_id == punto_venta_id,
            Inventario.fecha == fecha
        )
    ).first()

    if not inventario or inventario.cantidad == 0:
        return 0.0

    inventario_anterior = session.query(Inventario).filter(
        and_(
            Inventario.producto_id == producto_id,
            Inventario.punto_venta_id == punto_venta_id,
            Inventario.fecha < fecha
        )
    ).order_by(Inventario.fecha.desc()).first()

    if not inventario_anterior:
        return 0.0

    entradas_periodo = session.query(
        func.coalesce(func.sum(EntradaMercancia.cantidad), 0)
    ).filter(
        and_(
            EntradaMercancia.producto_id == producto_id,
            EntradaMercancia.punto_venta_id == punto_venta_id,
            EntradaMercancia.fecha > inventario_anterior.fecha,
            EntradaMercancia.fecha <= fecha
        )
    ).scalar()

    stock_promedio = (inventario.cantidad + inventario_anterior.cantidad) / 2

    if stock_promedio == 0:
        return 0.0

    rotacion = entradas_periodo / stock_promedio
    return round(rotacion, 2)


def detectar_patrones_estacionales(
    session: Session,
    producto_id: int,
    municipio_id: int
) -> Dict:
    promedios = {}
    for mes in range(1, 13):
        promedio = session.query(
            func.avg(Inventario.cantidad)
        ).join(PuntoVenta).filter(
            and_(
                Inventario.producto_id == producto_id,
                PuntoVenta.municipio_id == municipio_id,
                extract('month', Inventario.fecha) == mes
            )
        ).scalar()
        promedios[mes] = round(promedio or 0, 2)

    promedio_anual = sum(promedios.values()) / len(promedios) if promedios else 1

    meses_escasez = []
    meses_abundancia = []
    for mes, valor in promedios.items():
        if promedio_anual > 0:
            ratio = valor / promedio_anual
        else:
            ratio = 1.0
        if ratio < 0.97:
            meses_escasez.append(mes)
        elif ratio > 1.03:
            meses_abundancia.append(mes)

    return {
        "promedios_mensuales": promedios,
        "promedio_anual": round(promedio_anual, 2),
        "meses_escasez": meses_escasez,
        "meses_abundancia": meses_abundancia,
        "producto_id": producto_id,
        "municipio_id": municipio_id
    }


def calcular_nivel_stock_critico(
    session: Session,
    producto_id: int,
    punto_venta_id: int,
    umbral_critico: int = 7,
    umbral_alerta: int = 15
) -> Dict:
    ultimo_inventario = session.query(Inventario).filter(
        and_(
            Inventario.producto_id == producto_id,
            Inventario.punto_venta_id == punto_venta_id
        )
    ).order_by(Inventario.fecha.desc()).first()

    if not ultimo_inventario:
        return {"estado": "sin_datos", "cantidad": 0, "dias_stock": 0, "consumo_promedio_diario": 0}

    historial = session.query(Inventario).filter(
        and_(
            Inventario.producto_id == producto_id,
            Inventario.punto_venta_id == punto_venta_id
        )
    ).order_by(Inventario.fecha.asc()).all()

    if len(historial) < 2:
        return {"estado": "datos_insuficientes", "cantidad": ultimo_inventario.cantidad, "dias_stock": 0, "consumo_promedio_diario": 0}

    consumos = []
    for i in range(1, len(historial)):
        consumo = historial[i-1].cantidad - historial[i].cantidad
        consumos.append(max(0, consumo))

    consumo_promedio = sum(consumos) / len(consumos) if consumos else 0

    if consumo_promedio == 0:
        return {"estado": "sin_consumo", "cantidad": ultimo_inventario.cantidad, "dias_stock": 0, "consumo_promedio_diario": 0}

    dias_stock = ultimo_inventario.cantidad / (consumo_promedio / 30)

    if dias_stock < umbral_critico:
        estado = "critico"
    elif dias_stock < umbral_alerta:
        estado = "alerta"
    elif dias_stock < 30:
        estado = "normal"
    else:
        estado = "suficiente"

    return {
        "estado": estado,
        "cantidad": ultimo_inventario.cantidad,
        "dias_stock": round(dias_stock, 1),
        "consumo_promedio_diario": round(consumo_promedio / 30, 2)
    }


def generar_alertas_desabastecimiento(
    session: Session,
    umbral_dias: int = 15
) -> List[Dict]:
    alertas = []

    puntos_venta = session.query(PuntoVenta).all()
    productos = session.query(Producto).all()

    for pv in puntos_venta:
        for prod in productos:
            estado = calcular_nivel_stock_critico(
                session, prod.id, pv.id,
                umbral_critico=umbral_dias // 2,
                umbral_alerta=umbral_dias
            )

            if estado["estado"] in ["critico", "alerta"]:
                municipio = session.query(Municipio).filter(
                    Municipio.id == pv.municipio_id
                ).first()

                alertas.append({
                    "punto_venta": pv.nombre,
                    "municipio": municipio.nombre if municipio else "Desconocido",
                    "producto": prod.nombre,
                    "estado": estado["estado"],
                    "dias_stock": estado["dias_stock"],
                    "cantidad_actual": estado["cantidad"],
                    "consumo_diario": estado["consumo_promedio_diario"]
                })

    alertas.sort(key=lambda x: x["dias_stock"])
    return alertas


def calcular_estadisticas_producto_municipio(
    session: Session,
    producto_id: int,
    municipio_id: int,
    anio: int
) -> Dict:
    inventarios = session.query(Inventario).filter(
        and_(
            Inventario.producto_id == producto_id,
            extract('year', Inventario.fecha) == anio
        )
    ).join(PuntoVenta).filter(
        PuntoVenta.municipio_id == municipio_id
    ).all()

    if not inventarios:
        return {"sin_datos": True}

    cantidades = [inv.cantidad for inv in inventarios]

    return {
        "producto_id": producto_id,
        "municipio_id": municipio_id,
        "anio": anio,
        "promedio": round(sum(cantidades) / len(cantidades), 2),
        "minimo": round(min(cantidades), 2),
        "maximo": round(max(cantidades), 2),
        "registros": len(cantidades)
    }


if __name__ == "__main__":
    from app.database import SessionLocal
    session = SessionLocal()
    try:
        print("=" * 60)
        print("ALIMENDATA - MÉTRICAS ANALÍTICAS")
        print("=" * 60)

        from app.models.models import Producto, PuntoVenta

        alertas = generar_alertas_desabastecimiento(session)
        print(f"\nAlertas de desabastecimiento: {len(alertas)}")
        for a in alertas[:10]:
            print(f"  [{a['estado'].upper()}] {a['punto_venta']} ({a['municipio']}) - {a['producto']}: {a['dias_stock']} días")

        primer_producto = session.query(Producto).first()
        primer_pv = session.query(PuntoVenta).first()
        if primer_producto and primer_pv:
            rotacion = calcular_velocidad_rotacion(session, primer_producto.id, primer_pv.id, datetime.now().date())
            print(f"\nVelocidad de rotación (producto {primer_producto.nombre}, PV {primer_pv.id}): {rotacion}")

            stock = calcular_nivel_stock_critico(session, primer_producto.id, primer_pv.id)
            print(f"Nivel de stock crítico: {stock['estado']} ({stock['dias_stock']} días)")

        print("\nMétricas calculadas exitosamente.")
    finally:
        session.close()
