from pathlib import Path
import os
import processor.citi_banamex as cb_processor
import processor.data_processor as processor
import processor.graph_report as gp


def read_folder():
    _source_folder = "X:\\Edos Cuenta\\"

    data_transaction = cb_processor.read_files_in_folder(Path(_source_folder))

    # print("\n~~~~~~\n")
    #for d in data_transaction:
    #    print(d)

    gastos_concepto_mensual = processor.p_d(data_transaction)
    print("\n~~~~~~\n")
    gasto_anual_concepto = processor.gasto_anual(gastos_concepto_mensual)
    #gp.graph(gasto_anual_concepto)
    # gp.reporte_gastos(gasto_anual_concepto)
    gp.generar_archivo(gasto_anual_concepto)


if __name__ == '__main__':
    read_folder()

