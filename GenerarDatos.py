"""Genera datos ficticios para la demostración del patrón Index Table."""

import argparse
import json
from pathlib import Path


PRODUCTOS = [
    ("Laptop", 2500.00),
    ("Monitor", 800.00),
    ("Teclado", 150.00),
    ("Mouse", 75.00),
    ("Audífonos", 200.00),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directorio",
        type=Path,
        default=Path.cwd(),
        help="Directorio de salida (por defecto, el directorio actual)",
    )
    args = parser.parse_args()
    args.directorio.mkdir(parents=True, exist_ok=True)

    clientes = []
    pedidos = []
    for numero_cliente in range(1, 1001):
        cliente_id = f"C{numero_cliente:04d}"
        clientes.append({"_id": cliente_id, "nombre": f"Cliente {numero_cliente}"})
        for numero_pedido_cliente in range(10):
            numero_pedido = (numero_cliente - 1) * 10 + numero_pedido_cliente + 1
            producto, total = PRODUCTOS[(numero_pedido - 1) % len(PRODUCTOS)]
            pedidos.append({
                "_id": f"P{numero_pedido:06d}",
                "cliente_id": cliente_id,
                "producto": producto,
                "total": total,
            })

    archivos = [(args.directorio / "clientes.json", clientes),
                (args.directorio / "pedidos.json", pedidos)]
    existentes = [str(ruta) for ruta, _ in archivos if ruta.exists()]
    if existentes:
        parser.error("Ya existen archivos de salida: " + ", ".join(existentes))

    for ruta, datos in archivos:
        with ruta.open("x", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        print(f"{ruta}: {len(datos)} registros")


if __name__ == "__main__":
    main()
