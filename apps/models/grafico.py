import matplotlib.pyplot as plt
from apps.models.app_model import model_metadata
from apps.models.app_model import AppModel,model_metadata
from apps.models.objetivo import Objetivo,ObjetivoResult

@model_metadata({})
class Grafico(AppModel):
    def __init__(self, grafico_spec):
        self.nombre = grafico_spec["nombre"]
        self.formato = grafico_spec.get("extension", "svg")
        self.path = grafico_spec.get("nombre_archivo", self.nombre)

    def calcular(self, argumento):
        raise NotImplementedError(
            "Metodo a implementar por grafico no cumplido")

    def guardar(self):
        plt.savefig(self.get_path_completo(),
                    format=self.formato)
        plt.close()

    def get_path_completo(self):
        return f"{self.path}.{self.formato}"

class GraficoObjetivo(Grafico):

    def __init__(self, data):
        Grafico.__init__(self, data)

    def calcular(self, data):
        objetivo=data[0]
        objetivo_result=data[1]

        self.resultado = objetivo_result.valor
        self.nombre = objetivo.nombre

        return self.resultado

    def generar_grafico(self):

        _, ax = plt.subplots(subplot_kw=dict(aspect="equal"))

        etiquetas = ['Obtenido', 'Restante']
        porcentajes = [self.resultado, 100-self.resultado]

        def func(pct, allvals):
            return f"{pct:3.2f}%"

        explode = (0.1, 0) 
        wedges, _, _ = ax.pie(porcentajes,explode=explode ,autopct=lambda pct: func(pct, porcentajes),
                                          textprops=dict(color="w"),shadow=True,startangle=45,wedgeprops={"edgecolor": "0", 'linewidth': 1})

        ax.legend(wedges, etiquetas,
                  title="Porcentaje",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.title(f"OBJETIVO {self.nombre.upper()}")

        plt.tight_layout()

        Grafico.guardar(self)