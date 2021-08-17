# get indicador historico
```
{
    "id_indicador":1,
    "unidad_temporal":"horas",
    "precision":0.1
}
```
# get indicador
```
{
    "id_indicador":4,
    "muestras":4
    intervalo:null
}
{
    "id_indicador":1,
    "muestras":4
    intervalo:[2020,2021]
}
```
**returns**
```
[{
    "id_sensor":4,
    "valor":34,
    "unidad":"percentage"
},
{
    "id_sensor":1,
    "valor":67,
    "unidad":"percentage"
},
]
```

# get objetivo

GET /objetivos/id_objetivo
```
{
    "id_objetivo":3,
    "status":[alcanzado,pendiente,no alcanzado]
}
```

