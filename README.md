# SENSORIAL-RESTAPI

> Proyecto base para aplicaciones REST con python

![alt text](img/python.png)

## REQUERIMIENTOS

* **Python 3.7+**
* **Docker**

## EJECUCION

### PYTHON
* Ejecutar los sig. comandos:
```
virtualenv --python=python3.8 venv
venv/bin/activate
python app.py
```
Para quitar el virtualenv ejecutar el comando `deactivate`

### DOCKER

* Pararse en la ruta raiz del proyecto con docker instalado y funcionando
* Ejecutar `./scripts/build.sh`
* Ejecutar `docker run -it -p 5000:5000 sensorial-restapi:latest`

## CONFIGURACION
* La configuracion del proyecto se encuentra en *apps/configs/mapa_variables.py*,se pueden setear variables directamente en el mapa o por variable de entorno
* Para configurar una variable desde una variable de ambiente setear APP_NAME+NOMBRE_VARIABLE concatenado con guiones, por ej si el APP_NAME es **un_template** y se quiere setear la variable **una_variable**, la respectiva variable de entorno sera **UN-TEMPLATE-UNA-VARIABLE**
* Si se quiere crear una nueva variable y usarla dentro del codigo ir a *apps/configs/vars.py* y agregar un nuevo atributo que sea **NOMBRE_VARIABLE_EN_CODIGO="NOMBRE_VARIABLE_ENTORNO"** donde el primero es el nombre que se usara en el codigo y el segundo el que se usara como variable de ambiente (por lo gral. tienen el mismo nombre).
Luego para utilizarla en el codigo solo se ejecuta:
```
import apps.configs.configuration as conf
from apps.configs.vars import Vars

print(conf.get(Vars.NOMBRE_VARIABLE_EN_CODIGO))
```

## PAGINAS

[Docker python 3.7 apine](https://hub.docker.com/_/python)
