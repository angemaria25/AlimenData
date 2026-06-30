PRODUCTOS_CONFIG = {
    "arroz": {
        "categoria": "basicos",
        "unidad_medida": "kg",
        "vida_util_dias": 365,
        "consumo_mensual_kg": 1.7,
        "tasa_merma_almacen": 0.03,
        "tasa_perdida_transporte": 0.02,
        "tendencia_anual": 0.98,
        "factor_estacional": [0.80, 0.75, 0.75, 0.85, 0.95, 1.0, 1.10, 1.15, 1.05, 1.0, 1.05, 1.20],
    },
    "aceite": {
        "categoria": "basicos",
        "unidad_medida": "litros",
        "vida_util_dias": 180,
        "consumo_mensual_kg": 0.4,
        "tasa_merma_almacen": 0.04,
        "tasa_perdida_transporte": 0.01,
        "tendencia_anual": 0.97,
        "factor_estacional": [1.05, 0.85, 0.85, 0.90, 0.95, 1.0, 1.0, 1.05, 1.0, 1.10, 1.15, 1.30],
    },
    "frijoles": {
        "categoria": "basicos",
        "unidad_medida": "kg",
        "vida_util_dias": 365,
        "consumo_mensual_kg": 1.0,
        "tasa_merma_almacen": 0.025,
        "tasa_perdida_transporte": 0.015,
        "tendencia_anual": 0.99,
        "factor_estacional": [0.80, 0.70, 0.75, 0.85, 0.95, 1.05, 1.15, 1.20, 1.05, 1.0, 1.05, 1.25],
    },
    "azucar": {
        "categoria": "basicos",
        "unidad_medida": "kg",
        "vida_util_dias": 730,
        "consumo_mensual_kg": 0.6,
        "tasa_merma_almacen": 0.02,
        "tasa_perdida_transporte": 0.01,
        "tendencia_anual": 0.98,
        "factor_estacional": [1.0, 0.95, 0.95, 0.95, 1.0, 1.0, 1.0, 1.0, 0.95, 1.0, 1.10, 1.30],
    },
    "harina": {
        "categoria": "basicos",
        "unidad_medida": "kg",
        "vida_util_dias": 180,
        "consumo_mensual_kg": 0.5,
        "tasa_merma_almacen": 0.03,
        "tasa_perdida_transporte": 0.02,
        "tendencia_anual": 0.99,
        "factor_estacional": [0.85, 0.80, 0.80, 0.85, 0.95, 1.05, 1.15, 1.20, 1.05, 1.0, 1.05, 1.25],
    },
    "pollo": {
        "categoria": "proteinas",
        "unidad_medida": "kg",
        "vida_util_dias": 7,
        "consumo_mensual_kg": 0.65,
        "tasa_merma_almacen": 0.05,
        "tasa_perdida_transporte": 0.02,
        "tendencia_anual": 0.96,
        "factor_estacional": [1.40, 0.75, 0.70, 0.80, 0.90, 1.0, 1.15, 1.10, 0.95, 0.95, 1.20, 1.50],
    },
    "cerdo": {
        "categoria": "proteinas",
        "unidad_medida": "kg",
        "vida_util_dias": 5,
        "consumo_mensual_kg": 0.45,
        "tasa_merma_almacen": 0.04,
        "tasa_perdida_transporte": 0.02,
        "tendencia_anual": 0.97,
        "factor_estacional": [1.35, 0.75, 0.70, 0.80, 0.90, 1.0, 1.10, 1.05, 0.95, 0.95, 1.15, 1.45],
    },
    "huevos": {
        "categoria": "proteinas",
        "unidad_medida": "unidades",
        "vida_util_dias": 21,
        "consumo_mensual_kg": 0.4,
        "tasa_merma_almacen": 0.06,
        "tasa_perdida_transporte": 0.03,
        "tendencia_anual": 0.98,
        "factor_estacional": [1.25, 0.85, 0.80, 0.85, 0.95, 1.0, 1.10, 1.10, 1.0, 1.0, 1.10, 1.30],
    },
}

PROVINCIAS = [
    {"nombre": "Pinar del Río", "codigo": "PR"},
    {"nombre": "Artemisa", "codigo": "AR"},
    {"nombre": "La Habana", "codigo": "LH"},
    {"nombre": "Mayabeque", "codigo": "MY"},
    {"nombre": "Matanzas", "codigo": "MT"},
    {"nombre": "Villa Clara", "codigo": "VC"},
    {"nombre": "Cienfuegos", "codigo": "CF"},
    {"nombre": "Sancti Spíritus", "codigo": "SS"},
    {"nombre": "Ciego de Ávila", "codigo": "CA"},
    {"nombre": "Camagüey", "codigo": "CM"},
    {"nombre": "Las Tunas", "codigo": "LT"},
    {"nombre": "Holguín", "codigo": "HL"},
    {"nombre": "Granma", "codigo": "GR"},
    {"nombre": "Santiago de Cuba", "codigo": "SC"},
    {"nombre": "Guantánamo", "codigo": "GT"},
    {"nombre": "Isla de la Juventud", "codigo": "IJ"},
]

MUNICIPIOS_POR_PROVINCIA = {
    "Pinar del Río": [
        {"nombre": "Pinar del Río", "poblacion": 193500},
        {"nombre": "San Luis", "poblacion": 35000},
        {"nombre": "San Juan y Martínez", "poblacion": 22000},
        {"nombre": "Guane", "poblacion": 17000},
    ],
    "Artemisa": [
        {"nombre": "Artemisa", "poblacion": 85000},
        {"nombre": "Guanajay", "poblacion": 28000},
        {"nombre": "Candelaria", "poblacion": 20000},
        {"nombre": "San Antonio de los Baños", "poblacion": 47000},
    ],
    "La Habana": [
        {"nombre": "La Habana Vieja", "poblacion": 72000},
        {"nombre": "Centro Habana", "poblacion": 158000},
        {"nombre": "Plaza de la Revolución", "poblacion": 165000},
        {"nombre": "Regla", "poblacion": 46000},
        {"nombre": "La Lisa", "poblacion": 133000},
        {"nombre": "Playa", "poblacion": 175000},
        {"nombre": "Diez de Octubre", "poblacion": 215000},
        {"nombre": "Cerro", "poblacion": 85000},
        {"nombre": "Marianao", "poblacion": 95000},
        {"nombre": "San Miguel del Padrón", "poblacion": 155000},
    ],
    "Mayabeque": [
        {"nombre": "San José de las Lajas", "poblacion": 75000},
        {"nombre": "Bejucal", "poblacion": 26000},
        {"nombre": "Santa Cruz del Norte", "poblacion": 32000},
    ],
    "Matanzas": [
        {"nombre": "Matanzas", "poblacion": 155000},
        {"nombre": "Cárdenas", "poblacion": 140000},
        {"nombre": "Sagua la Grande", "poblacion": 55000},
    ],
    "Villa Clara": [
        {"nombre": "Santa Clara", "poblacion": 235000},
        {"nombre": "Placetas", "poblacion": 42000},
        {"nombre": "Remedios", "poblacion": 25000},
    ],
    "Cienfuegos": [
        {"nombre": "Cienfuegos", "poblacion": 150000},
        {"nombre": "Abreus", "poblacion": 33000},
    ],
    "Sancti Spíritus": [
        {"nombre": "Sancti Spíritus", "poblacion": 130000},
        {"nombre": "Trinidad", "poblacion": 75000},
    ],
    "Ciego de Ávila": [
        {"nombre": "Ciego de Ávila", "poblacion": 150000},
        {"nombre": "Morón", "poblacion": 70000},
    ],
    "Camagüey": [
        {"nombre": "Camagüey", "poblacion": 320000},
        {"nombre": "Florida", "poblacion": 55000},
        {"nombre": "Guáimaro", "poblacion": 57000},
    ],
    "Las Tunas": [
        {"nombre": "Las Tunas", "poblacion": 155000},
        {"nombre": "Puerto Padre", "poblacion": 90000},
    ],
    "Holguín": [
        {"nombre": "Holguín", "poblacion": 325000},
        {"nombre": "Gibara", "poblacion": 72000},
        {"nombre": "Banes", "poblacion": 82000},
    ],
    "Granma": [
        {"nombre": "Bayamo", "poblacion": 245000},
        {"nombre": "Manzanillo", "poblacion": 135000},
        {"nombre": "Jiguaní", "poblacion": 60000},
    ],
    "Santiago de Cuba": [
        {"nombre": "Santiago de Cuba", "poblacion": 510000},
        {"nombre": "Palma Soriano", "poblacion": 88000},
        {"nombre": "San Luis", "poblacion": 85000},
    ],
    "Guantánamo": [
        {"nombre": "Guantánamo", "poblacion": 255000},
        {"nombre": "Baracoa", "poblacion": 80000},
    ],
    "Isla de la Juventud": [
        {"nombre": "Nueva Gerona", "poblacion": 70000},
    ],
}

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

ANIOS = range(2011, 2025)
