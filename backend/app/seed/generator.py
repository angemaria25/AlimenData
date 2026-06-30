import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from app.seed.config import PRODUCTOS_CONFIG, PROVINCIAS, MUNICIPIOS_POR_PROVINCIA, ANIOS, MESES


def generar_datos_historicos(output_dir="database/seeds"):
    os.makedirs(output_dir, exist_ok=True)
    
    all_inventarios = []
    all_asignaciones = []
    all_entradas = []
    all_mermas = []
    all_perdidas = []
    
    asignacion_id_counter = 1
    
    producto_id_map = {}
    municipio_id_map = {}
    almacen_id_map = {}
    punto_venta_id_map = {}
    
    producto_counter = 1
    for producto in PRODUCTOS_CONFIG.keys():
        producto_id_map[producto] = producto_counter
        producto_counter += 1
    
    municipio_counter = 1
    for provincia in PROVINCIAS:
        for municipio in MUNICIPIOS_POR_PROVINCIA[provincia["nombre"]]:
            municipio_id_map[municipio["nombre"]] = municipio_counter
            municipio_counter += 1
    
    almacen_counter = 1
    for provincia in PROVINCIAS:
        almacen_id_map[provincia["nombre"]] = almacen_counter
        almacen_counter += 1
    
    punto_venta_counter = 1
    for provincia in PROVINCIAS:
        for municipio in MUNICIPIOS_POR_PROVINCIA[provincia["nombre"]]:
            num_bodegas = max(3, municipio["poblacion"] // 20000)
            for i in range(num_bodegas):
                punto_venta_id = punto_venta_counter
                punto_venta_id_map[f"{municipio['nombre']}_bodega_{i+1}"] = punto_venta_counter
                punto_venta_counter += 1
    
    print(f"Generando datos para {len(PRODUCTOS_CONFIG)} productos...")
    print(f"Total municipios: {len(municipio_id_map)}")
    print(f"Total puntos de venta: {len(punto_venta_id_map)}")
    
    for producto_name, params in PRODUCTOS_CONFIG.items():
        producto_id = producto_id_map[producto_name]
        
        for provincia in PROVINCIAS:
            almacen_id = almacen_id_map[provincia["nombre"]]
            
            for municipio in MUNICIPIOS_POR_PROVINCIA[provincia["nombre"]]:
                municipio_id = municipio_id_map[municipio["nombre"]]
                poblacion = municipio["poblacion"]
                
                inventario_acumulado = 0
                
                for anio in ANIOS:
                    for mes_idx, mes in enumerate(MESES):
                        mes_num = mes_idx + 1
                        fecha = datetime(anio, mes_num, 1).date()
                        
                        tendencia = params["tendencia_anual"] ** (anio - 2011)
                        factor_est = params["factor_estacional"][mes_idx]
                        
                        demanda = (
                            poblacion * params["consumo_mensual_kg"] * factor_est * tendencia
                        )
                        ruido = np.random.normal(0, demanda * 0.05)
                        demanda = max(0, demanda + ruido)
                        
                        entradas = demanda * 1.1 + np.random.normal(0, demanda * 0.03)
                        entradas = max(0, entradas)
                        
                        merma = entradas * params["tasa_merma_almacen"]
                        merma += np.random.normal(0, merma * 0.1)
                        merma = max(0, merma)
                        
                        perdida_transporte = entradas * params["tasa_perdida_transporte"]
                        perdida_transporte += np.random.normal(0, perdida_transporte * 0.1)
                        perdida_transporte = max(0, perdida_transporte)
                        
                        disponible = entradas - merma - perdida_transporte
                        inventario_acumulado = inventario_acumulado + disponible - demanda
                        inventario_acumulado = max(0, inventario_acumulado)
                        
                        for pv_idx in range(max(1, poblacion // 20000)):
                            pv_key = f"{municipio['nombre']}_bodega_{pv_idx+1}"
                            pv_id = punto_venta_id_map.get(pv_key)
                            if pv_id is None:
                                continue
                            
                            pv_share = demanda / max(1, poblacion // 20000)
                            pv_inventario = inventario_acumulado / max(1, poblacion // 20000)
                            
                            inventario_id = len(all_inventarios) + 1
                            all_inventarios.append({
                                "id": inventario_id,
                                "producto_id": producto_id,
                                "punto_venta_id": pv_id,
                                "fecha": fecha,
                                "cantidad": round(max(0, pv_inventario), 2),
                            })
                            
                            all_entradas.append({
                                "producto_id": producto_id,
                                "punto_venta_id": pv_id,
                                "fecha": fecha,
                                "cantidad": round(max(0, pv_share), 2),
                                "proveedor": f"Distribuidora {provincia['nombre']}",
                            })
                            
                            all_mermas.append({
                                "inventario_id": inventario_id,
                                "cantidad": round(max(0, merma / max(1, poblacion // 20000)), 2),
                                "motivo": np.random.choice([
                                    "Vencimiento", "Daño por manipulación", 
                                    "Falta de refrigeración", "Plagas"
                                ]),
                                "fecha": datetime(anio, mes_num, 15),
                            })
                            
                            asignacion_id = asignacion_id_counter
                            all_asignaciones.append({
                                "id": asignacion_id,
                                "producto_id": producto_id,
                                "almacen_origen_id": almacen_id,
                                "punto_venta_destino_id": pv_id,
                                "fecha": fecha,
                                "cantidad": round(max(0, pv_share * 1.05), 2),
                                "estado": "completada",
                            })
                            
                            all_perdidas.append({
                                "asignacion_id": asignacion_id,
                                "cantidad": round(max(0, perdida_transporte / max(1, poblacion // 20000)), 2),
                                "motivo": np.random.choice([
                                    "Deterioro en transporte", "Accidente vehicular",
                                    "Condiciones climáticas", "Demora en entrega"
                                ]),
                                "fecha": datetime(anio, mes_num, 20),
                            })
                            asignacion_id_counter += 1
    
    print("Generando DataFrames...")
    df_inventarios = pd.DataFrame(all_inventarios)
    df_entradas = pd.DataFrame(all_entradas)
    df_mermas = pd.DataFrame(all_mermas)
    df_asignaciones = pd.DataFrame(all_asignaciones)
    df_perdidas = pd.DataFrame(all_perdidas)
    
    df_inventarios["id"] = df_inventarios["id"].astype("int32")
    df_inventarios["producto_id"] = df_inventarios["producto_id"].astype("int32")
    df_inventarios["punto_venta_id"] = df_inventarios["punto_venta_id"].astype("int32")
    df_inventarios["cantidad"] = df_inventarios["cantidad"].astype("float32")
    df_inventarios["fecha"] = pd.to_datetime(df_inventarios["fecha"]).dt.date
    
    df_entradas["producto_id"] = df_entradas["producto_id"].astype("int32")
    df_entradas["punto_venta_id"] = df_entradas["punto_venta_id"].astype("int32")
    df_entradas["cantidad"] = df_entradas["cantidad"].astype("float32")
    df_entradas["fecha"] = pd.to_datetime(df_entradas["fecha"]).dt.date
    
    df_mermas["inventario_id"] = df_mermas["inventario_id"].astype("int32")
    df_mermas["cantidad"] = df_mermas["cantidad"].astype("float32")
    df_mermas["fecha"] = pd.to_datetime(df_mermas["fecha"])
    
    df_asignaciones["id"] = df_asignaciones["id"].astype("int32")
    df_asignaciones["producto_id"] = df_asignaciones["producto_id"].astype("int32")
    df_asignaciones["almacen_origen_id"] = df_asignaciones["almacen_origen_id"].astype("int32")
    df_asignaciones["punto_venta_destino_id"] = df_asignaciones["punto_venta_destino_id"].astype("int32")
    df_asignaciones["cantidad"] = df_asignaciones["cantidad"].astype("float32")
    df_asignaciones["fecha"] = pd.to_datetime(df_asignaciones["fecha"]).dt.date
    
    df_perdidas["asignacion_id"] = df_perdidas["asignacion_id"].astype("int32")
    df_perdidas["cantidad"] = df_perdidas["cantidad"].astype("float32")
    df_perdidas["fecha"] = pd.to_datetime(df_perdidas["fecha"])
    
    print("Guardando archivos CSV...")
    df_inventarios.to_csv(os.path.join(output_dir, "inventarios.csv"), index=False)
    df_entradas.to_csv(os.path.join(output_dir, "entradas.csv"), index=False)
    df_mermas.to_csv(os.path.join(output_dir, "mermas.csv"), index=False)
    df_asignaciones.to_csv(os.path.join(output_dir, "asignaciones.csv"), index=False)
    df_perdidas.to_csv(os.path.join(output_dir, "perdidas_transporte.csv"), index=False)
    
    print("Generando archivos de referencia...")
    df_provincias = pd.DataFrame(PROVINCIAS)
    df_provincias["id"] = range(1, len(PROVINCIAS) + 1)
    df_provincias.to_csv(os.path.join(output_dir, "provincias.csv"), index=False)
    
    df_municipios = []
    municipio_id = 1
    for prov_idx, provincia in enumerate(PROVINCIAS, 1):
        for municipio in MUNICIPIOS_POR_PROVINCIA[provincia["nombre"]]:
            df_municipios.append({
                "id": municipio_id,
                "nombre": municipio["nombre"],
                "provincia_id": prov_idx,
                "poblacion": municipio["poblacion"],
            })
            municipio_id += 1
    pd.DataFrame(df_municipios).to_csv(os.path.join(output_dir, "municipios.csv"), index=False)
    
    df_productos = []
    for idx, (producto_name, params) in enumerate(PRODUCTOS_CONFIG.items(), 1):
        df_productos.append({
            "id": idx,
            "nombre": producto_name,
            "categoria": params["categoria"],
            "unidad_medida": params["unidad_medida"],
            "vida_util_dias": params["vida_util_dias"],
        })
    pd.DataFrame(df_productos).to_csv(os.path.join(output_dir, "productos.csv"), index=False)
    
    print(f"Archivos generados en {output_dir}/")
    print(f"  - inventarios.csv: {len(df_inventarios)} registros")
    print(f"  - entradas.csv: {len(df_entradas)} registros")
    print(f"  - mermas.csv: {len(df_mermas)} registros")
    print(f"  - asignaciones.csv: {len(df_asignaciones)} registros")
    print(f"  - perdidas_transporte.csv: {len(df_perdidas)} registros")
    print(f"  - provincias.csv: {len(df_provincias)} registros")
    print(f"  - municipios.csv: {len(df_municipios)} registros")
    print(f"  - productos.csv: {len(df_productos)} registros")
    
    return {
        "inventarios": df_inventarios,
        "entradas": df_entradas,
        "mermas": df_mermas,
        "asignaciones": df_asignaciones,
        "provincias": df_provincias,
        "municipios": pd.DataFrame(df_municipios),
        "productos": pd.DataFrame(df_productos),
    }


if __name__ == "__main__":
    generar_datos_historicos()
