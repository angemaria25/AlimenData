"""Initial migration - Create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-06-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create Provincias table
    op.create_table(
        'provincias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('codigo', sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo'),
        sa.UniqueConstraint('nombre')
    )

    # Create Municipios table
    op.create_table(
        'municipios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('provincia_id', sa.Integer(), nullable=False),
        sa.Column('poblacion', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['provincia_id'], ['provincias.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Productos table
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('categoria', sa.String(length=50), nullable=False),
        sa.Column('unidad_medida', sa.String(length=20), nullable=False),
        sa.Column('vida_util_dias', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )

    # Create Almacenes Centrales table
    op.create_table(
        'almacenes_centrales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('provincia_id', sa.Integer(), nullable=False),
        sa.Column('capacidad_max', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['provincia_id'], ['provincias.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Puntos de Venta table
    op.create_table(
        'puntos_venta',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('municipio_id', sa.Integer(), nullable=False),
        sa.Column('capacidad_max', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['municipio_id'], ['municipios.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('ix_puntos_venta_municipio', 'puntos_venta', ['municipio_id'])

    # Create Inventarios table (with Date field for time series)
    op.create_table(
        'inventarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('punto_venta_id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id']),
        sa.ForeignKeyConstraint(['punto_venta_id'], ['puntos_venta.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Asignaciones table (with Date field for time series)
    op.create_table(
        'asignaciones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('almacen_origen_id', sa.Integer(), nullable=False),
        sa.Column('punto_venta_destino_id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.Column('estado', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['almacen_origen_id'], ['almacenes_centrales.id']),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id']),
        sa.ForeignKeyConstraint(['punto_venta_destino_id'], ['puntos_venta.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Entradas de Mercancia table (with Date field for time series)
    op.create_table(
        'entradas_mercancia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('punto_venta_id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.Column('proveedor', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id']),
        sa.ForeignKeyConstraint(['punto_venta_id'], ['puntos_venta.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Mermas table
    op.create_table(
        'mermas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inventario_id', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.Column('motivo', sa.String(length=200), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['inventario_id'], ['inventarios.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Perdidas por Transporte table
    op.create_table(
        'perdidas_transporte',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asignacion_id', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.Column('motivo', sa.String(length=200), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['asignacion_id'], ['asignaciones.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better performance
    op.create_index('ix_inventarios_producto', 'inventarios', ['producto_id'])
    op.create_index('ix_inventarios_punto_venta', 'inventarios', ['punto_venta_id'])
    op.create_index('ix_inventarios_fecha', 'inventarios', ['fecha'])
    op.create_index('ix_asignaciones_producto', 'asignaciones', ['producto_id'])
    op.create_index('ix_asignaciones_fecha', 'asignaciones', ['fecha'])
    op.create_index('ix_entradas_producto', 'entradas_mercancia', ['producto_id'])
    op.create_index('ix_entradas_fecha', 'entradas_mercancia', ['fecha'])


def downgrade() -> None:
    op.drop_index('ix_puntos_venta_municipio')
    op.drop_table('perdidas_transporte')
    op.drop_table('mermas')
    op.drop_table('entradas_mercancia')
    op.drop_table('asignaciones')
    op.drop_table('inventarios')
    op.drop_table('puntos_venta')
    op.drop_table('almacenes_centrales')
    op.drop_table('productos')
    op.drop_table('municipios')
    op.drop_table('provincias')
