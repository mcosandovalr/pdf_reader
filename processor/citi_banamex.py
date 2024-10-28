import os.path
import re
from pathlib import Path
from typing import List
from pypdf import PdfReader
from models.estado_cuenta import Transaccion


def search_in_page(page):
    # Mensualidad * / Tipos de Cambio Moneda Ext. Divisas
    # busca que comience similar a: "May 12", "Jun 1"
    pattern = r"^([A-Z]{1})([a-z]{2})(\s+)(\d+)"
    _transactions = []
    text = page.extract_text()
    rows = text.split("\n")
    for row in rows:
        if re.match(pattern, row):
            _transactions.append(row)
            # print(f"{row}")
    return _transactions


def read_files_in_folder(path: Path):
    try:
        if not os.path.exists(path):
            print(f"No existe el path: {path}")
        elif not os.path.isdir(path):
            print(f"el path no es un folder.   Revisa el valor: {path}")
        else:
            _transacciones = []
            # revisar los archivos que existen
            ext = "*.pdf"
            print("Se encontraron los siguientes estados de cuenta:")
            edo_cuentas = [f for f in Path(path).glob(ext)]
            for i, edo_cuenta in enumerate(edo_cuentas):
                print(f"{i + 1} - {edo_cuenta}")

            print("procesando todos los archivos")
            for edo_cuenta in edo_cuentas:
                _transacciones.extend(process_file(edo_cuenta))
            return _transacciones
    except Exception as e:
        print(f"[ERR] {e}")


def process_file(file_path):
    reader = PdfReader(file_path)

    # numero de paginas del pdf
    page_count = len(reader.pages)
    transactions = []
    for page_obj in range(page_count):
        page = reader.pages[page_obj]
        tx = search_in_page(page)
        if tx:
            transactions.extend(tx)

    _transacciones: List[Transaccion] =[]
    for tx in transactions:
        # imprimimos la transaccion
        # print(tx)
        not_allowed = ['ABONO...GRACIAS']
        if any(palabra in tx for palabra in not_allowed):
            continue
        data = tx.split(" ")
        t = Transaccion()
        month = data[0]
        day_chain = str()  # "" # la usaremos para armar
        set_concepto = False
        concepto_chain = str()
        set_giro = False
        giro_chain = str()
        cantidad_chain = str()
        set_cantidad = False

        for i, character in enumerate(data[1:], start=1):
            if character:
                # obteniendo el dia
                if not day_chain:  # not empty
                    pattern = r"\d{1}"
                    if re.match(pattern, character):  # revisar si ya tenemos algun valor para el dia
                        day_chain = character
                        t.fecha = f"{month} {day_chain}"
                        t.mes = month
                        t.dia = day_chain
                        continue # next index
                elif not set_concepto:
                    if not concepto_chain:
                        concepto_chain = character
                    else:
                        concepto_chain = f"{concepto_chain} {character}"
                    if i + 1 < len(data):
                        next_character = data[i + 1]
                        if not next_character:  # si es una cadena vacia, ya completamos el dia y nos podemos salir
                            set_concepto = True
                            t.concepto = concepto_chain
                            continue
                # sacar primero el total para utilizarlo de referencia mas adelante al tratar de sacar los demas datos
                # si los demas datos tienen el valor del total, entonces no venian y los seteamos a None
                elif not set_giro:
                    if not giro_chain:
                        if character:
                            giro_chain = character
                    else:
                        giro_chain = f"{giro_chain}{character}"
                    if i + 1 < len(data):
                        next_character = data[i + 1]
                        pattern = r"^\d{1,3}(,\d{3})*(\.\d{2})$"
                        if re.match(pattern, next_character):  # si es una cadena vacia, ya completamos el dia y nos podemos salir
                            set_giro = True
                            t.giro_negocio = giro_chain
                            continue
                elif not set_cantidad:
                    if not cantidad_chain:
                        pattern = r"^\d{1,3}(,\d{3})*(\.\d{2})$"
                        if re.match(pattern, character):
                            # eliminar coma de la cadena
                            cantidad_chain = character.replace(',','')
                            t.cantidad_pesos = float(cantidad_chain)
                            set_cantidad = True
                            _transacciones.append(t)
                            continue
    return _transacciones

