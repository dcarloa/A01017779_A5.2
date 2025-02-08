"""
Este modulo calcula el costo de  las ventas basado en los precios.
Los resultados se muestran en pantalla y se guardan en SalesResults.txt.
Maneja errores en los archivos y mide el tiempo de ejecucion.
"""

import sys
import json
import time


def leer_json(ruta_archivo):
    """Lee un archivo JSON y maneja errores en la lectura."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo '{ruta_archivo}'.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{ruta_archivo}': formato JSON invalido.")
        sys.exit(1)


def normalizar_texto(texto):
    """Convierte el texto a minusculas y elimina espacios extras."""
    return texto.strip().lower()


def calcular_total_ventas(catalogo, ventas):
    """Calcula el costo de las ventas basado en los precios."""
    total_ventas = 0.0
    ventas_validas = 0
    ventas_invalidas = 0

    # Convertir la lista del catalogo en un diccionario clave-valor
    catalogo_normalizado = {
        normalizar_texto(item["title"]): item["price"]
        for item in catalogo
    }

    for venta in ventas:
        producto = venta.get("Product", "")
        cantidad = venta.get("Quantity")

        # Normalizar el nombre del producto
        producto_normalizado = normalizar_texto(producto)

        if not isinstance(producto, str) or not isinstance(
            cantidad, (int, float)
        ) or cantidad <= 0:
            print(
                f"Error: Venta invalida {venta}. "
                "Se omitira."
            )
            ventas_invalidas += 1
            continue

        if producto_normalizado in catalogo_normalizado:
            total_ventas += (
                catalogo_normalizado[producto_normalizado] * cantidad
            )
            ventas_validas += 1
        else:
            print(
                f"Error: Producto '{producto}' "
                "no encontrado en el catalogo. Se omitira."
            )
            ventas_invalidas += 1

    return total_ventas, ventas_validas, ventas_invalidas


def guardar_resultados(nombre_archivo, total, validas, invalidas, duracion):
    """Guarda los resultados en un archivo de texto."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("=== Resultados de Ventas ===\n")
        archivo.write(f"Total de ventas: ${total:.2f}\n")
        archivo.write(f"Ventas procesadas correctamente: {validas}\n")
        archivo.write(f"Ventas con errores: {invalidas}\n")
        archivo.write(
            f"\nTiempo de ejecucion: {duracion:.6f} segundos\n"
        )


def principal():
    """Ejecuta el programa principal."""
    if len(sys.argv) != 3:
        print(
            "Uso correcto: python A01017779_A5.2.py "
            "catalogo.json ventas.json"
        )
        sys.exit(1)

    archivo_catalogo = sys.argv[1]
    archivo_ventas = sys.argv[2]

    inicio_tiempo = time.time()

    catalogo_precios = leer_json(archivo_catalogo)
    ventas_registradas = leer_json(archivo_ventas)

    total, validas, invalidas = calcular_total_ventas(
        catalogo_precios, ventas_registradas
    )

    tiempo_total = time.time() - inicio_tiempo

    print("\n=== Resultados de Ventas ===")
    print(f"Total de ventas: ${total:.2f}")
    print(f"Ventas procesadas correctamente: {validas}")
    print(f"Ventas con errores: {invalidas}")
    print(f"Tiempo de ejecucion: {tiempo_total:.6f} segundos")

    guardar_resultados(
        "SalesResults.txt", total, validas, invalidas, tiempo_total
    )


if __name__ == "__main__":
    principal()
