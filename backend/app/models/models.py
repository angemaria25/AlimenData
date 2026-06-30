from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    codigo = Column(String(10), nullable=False, unique=True)

    municipios = relationship("Municipio", back_populates="provincia")
    almacenes = relationship("AlmacenCentral", back_populates="provincia")


class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    poblacion = Column(Integer, nullable=False)

    provincia = relationship("Provincia", back_populates="municipios")
    puntos_venta = relationship("PuntoVenta", back_populates="municipio")


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    categoria = Column(String(50), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    vida_util_dias = Column(Integer, nullable=False)

    inventarios = relationship("Inventario", back_populates="producto")
    asignaciones = relationship("Asignacion", back_populates="producto")
    entradas = relationship("EntradaMercancia", back_populates="producto")


class AlmacenCentral(Base):
    __tablename__ = "almacenes_centrales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    capacidad_max = Column(Float, nullable=False)

    provincia = relationship("Provincia", back_populates="almacenes")
    asignaciones = relationship("Asignacion", back_populates="almacen_origen")


class PuntoVenta(Base):
    __tablename__ = "puntos_venta"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)  # bodega o mercado
    municipio_id = Column(Integer, ForeignKey("municipios.id"), nullable=False)
    capacidad_max = Column(Float, nullable=False)

    municipio = relationship("Municipio", back_populates="puntos_venta")
    inventarios = relationship("Inventario", back_populates="punto_venta")
    entradas = relationship("EntradaMercancia", back_populates="punto_venta")


class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    punto_venta_id = Column(Integer, ForeignKey("puntos_venta.id"), nullable=False)
    fecha = Column(Date, nullable=False)  # Campo Date para series temporales
    cantidad = Column(Float, nullable=False)

    producto = relationship("Producto", back_populates="inventarios")
    punto_venta = relationship("PuntoVenta", back_populates="inventarios")
    mermas = relationship("Merma", back_populates="inventario")


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    almacen_origen_id = Column(Integer, ForeignKey("almacenes_centrales.id"), nullable=False)
    punto_venta_destino_id = Column(Integer, ForeignKey("puntos_venta.id"), nullable=False)
    fecha = Column(Date, nullable=False)  # Campo Date para series temporales
    cantidad = Column(Float, nullable=False)
    estado = Column(String(20), nullable=False, default="completada")

    producto = relationship("Producto", back_populates="asignaciones")
    almacen_origen = relationship("AlmacenCentral", back_populates="asignaciones")
    perdidas = relationship("PerdidaTransporte", back_populates="asignacion")


class EntradaMercancia(Base):
    __tablename__ = "entradas_mercancia"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    punto_venta_id = Column(Integer, ForeignKey("puntos_venta.id"), nullable=False)
    fecha = Column(Date, nullable=False)  # Campo Date para series temporales
    cantidad = Column(Float, nullable=False)
    proveedor = Column(String(100), nullable=True)

    producto = relationship("Producto", back_populates="entradas")
    punto_venta = relationship("PuntoVenta", back_populates="entradas")


class Merma(Base):
    __tablename__ = "mermas"

    id = Column(Integer, primary_key=True, index=True)
    inventario_id = Column(Integer, ForeignKey("inventarios.id"), nullable=False)
    cantidad = Column(Float, nullable=False)
    motivo = Column(String(200), nullable=False)
    fecha = Column(DateTime, nullable=False)

    inventario = relationship("Inventario", back_populates="mermas")


class PerdidaTransporte(Base):
    __tablename__ = "perdidas_transporte"

    id = Column(Integer, primary_key=True, index=True)
    asignacion_id = Column(Integer, ForeignKey("asignaciones.id"), nullable=False)
    cantidad = Column(Float, nullable=False)
    motivo = Column(String(200), nullable=False)
    fecha = Column(DateTime, nullable=False)

    asignacion = relationship("Asignacion", back_populates="perdidas")
