from collections import defaultdict
from typing import List
from models.estado_cuenta import Transaccion, Gasto


def p_d(data_transaction: List[Transaccion]):
    gastos_concepto_mensual = defaultdict(float)

    for transaccion in data_transaction:
        try:
            monto = float(transaccion.cantidad_pesos)
        except ValueError:
            print(f"[ERR] el valor de cantidad_pesos no es valido: {transaccion.cantidad_pesos}")
            continue

        # creamos una clave unica que sea (mes, concepto.nombre)
        clave = (transaccion.mes, transaccion.concepto)
        gastos_concepto_mensual[clave] += monto

    # imprimir resultados por mes y concepto
    #for (mes, concepto), total in gastos_concepto_mensual.items():
        #print(f"{mes} {concepto} ${total:.2f}")

    return gastos_concepto_mensual


def gasto_anual(gastos_concepto_mensual):
    gasto_anual_concepto = defaultdict(float)

    for (mes, concepto), total in gastos_concepto_mensual.items():
        gasto_anual_concepto[concepto] += total

    for concepto, total in gasto_anual_concepto.items():
        print(f" >    {concepto}: {total:.2f}")

    lista_gastos_anual = [Gasto(concepto, gasto) for concepto, gasto in gasto_anual_concepto.items()]
    return lista_gastos_anual
    #return gasto_anual_concepto

