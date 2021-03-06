import matplotlib.pyplot as plt
from apps.models.app_model import model_metadata
from apps.models.app_model import AppModel,model_metadata
from apps.models.objetivo import Objetivo,ObjetivoResult
import numpy

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

        self.resultado = [objetivo_result.valor,objetivo_result.valor_esperado]
        self.nombre = objetivo.nombre

        return self.resultado

    def generar_grafico(self):

        _, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
        explode = [0.1,0.1] 

        etiquetas = ['Obtenido', 'Necesario']
        porcentajes = [self.resultado[0],self.resultado[1]]

        colors = []

        red='#EC2647'
        blue='#2F9ED5'
        green='#19CE1F'
        orange='#E47327'

        if self.resultado[0]>=self.resultado[1]:
            colors.append(green)
        else:
            colors.append(red)

        colors.append(orange)

        if self.resultado[0]<100:
            etiquetas.append("Restante")
            porcentajes.append(100-self.resultado[0])
            explode.append(0)
            colors.append(blue)

        def func(val,allvals):
            a  = allvals[ numpy.abs(allvals - val/100.*sum(allvals)).argmin() ]
            return f"{a:3.2f}%"


        wedges, _, _ = ax.pie(porcentajes,explode=explode ,colors=colors,autopct=lambda pct: func(pct, porcentajes),
                                          textprops=dict(color="w",backgroundcolor="k"),shadow=True,startangle=45,wedgeprops={"edgecolor": "0", 'linewidth': 1})

        ax.legend(wedges, etiquetas,
                  title="Porcentaje",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.title(f"{self.nombre.upper()}")

        plt.tight_layout()

        Grafico.guardar(self)