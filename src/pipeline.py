import os
import psycopg
from decimal import Decimal
import pandas as pd
from pathlib import Path
import logging

# Configuración de registros de ejecución
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ubicación de los archivos
BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVO_CSV = BASE_DIR / "data" / "ventas.csv"


# EXTRACCIÓN
def extraer_datos():
    datos = pd.read_csv(ARCHIVO_CSV)

    logging.info(f"Registros extraídos: {len(datos)}")

    return datos


# TRANSFORMACIÓN
def transformar_datos(datos):
    registros_iniciales = len(datos)

    # Convertir tipos de datos
    datos["fecha"] = pd.to_datetime(
        datos["fecha"], errors="coerce"
    )

    datos["cantidad"] = pd.to_numeric(
        datos["cantidad"], errors="coerce"
    )

    datos["precio_unitario"] = pd.to_numeric(
        datos["precio_unitario"], errors="coerce"
    )

    # Eliminar registros incompletos
    datos = datos.dropna()

    # Eliminar cantidades y precios inválidos
    datos = datos[
        (datos["cantidad"] > 0) &
        (datos["precio_unitario"] > 0)
    ].copy()

    # Eliminar ventas duplicadas
    datos = datos.drop_duplicates(
        subset=["id_venta"]
    ).copy()

    # Convertir cantidades a números enteros
    datos["cantidad"] = datos["cantidad"].astype(int)

    # Calcular el importe de cada venta
    datos["total"] = (
        datos["cantidad"] * datos["precio_unitario"]
    )

    logging.info(f"Registros válidos: {len(datos)}")

    logging.info(
        f"Registros descartados: "
        f"{registros_iniciales - len(datos)}"
    )

    return datos


# CARGA DE DATOS EN POSTGRESQL
def cargar_datos(datos):

    logging.info("Conectando con PostgreSQL")

    with psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    ) as conexion:

        with conexion.cursor() as cursor:

            consulta = """
                INSERT INTO ventas (
                    id_venta,
                    fecha,
                    producto,
                    cantidad,
                    precio_unitario,
                    ciudad
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_venta) DO NOTHING;
            """

            registros = [
                (
                    int(fila.id_venta),
                    fila.fecha.date(),
                    str(fila.producto),
                    int(fila.cantidad),
                    Decimal(str(fila.precio_unitario)),
                    str(fila.ciudad)
                )
                for fila in datos.itertuples(index=False)
            ]

            cursor.executemany(consulta, registros)

            logging.info(
                f"Registros nuevos insertados: {cursor.rowcount}"
            )

    logging.info("Carga de datos completada")

# EJECUCIÓN DEL PIPELINE
def main():
    logging.info("Iniciando pipeline ETL")

    datos = extraer_datos()
    datos_limpios = transformar_datos(datos)

    print(datos_limpios.to_string(index=False))

    cargar_datos(datos_limpios)

    logging.info("Pipeline ETL completado correctamente")

if __name__ == "__main__":
    main()
