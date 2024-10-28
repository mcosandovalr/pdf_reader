from dataclasses import dataclass


class Document:
    rows: [str]


class Concepto:
    nombre: str
    codigo: str


@dataclass
class Gasto:
    concepto: str
    gasto: float

    def __init__(self, concepto: str, gasto: float):
        self.concepto = concepto
        self.gasto = gasto


@dataclass
class GastoMensual(Gasto): #refactorizar
    mes: str

class Transaccion:
    fecha: str # obtener mes y dia
    mes: str
    dia: str
    concepto: str
    detalles: str
    giro_negocio: str
    poblacion_rfc: str
    otras_divisas: str
    cantidad_pesos: float

    def __str__(self):
        return f"{self.mes} {self.dia} {self.concepto} {self.cantidad_pesos}"

