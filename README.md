# README

## Objetivo
La comisión de convivencia se encarga de gestionar varias tareas. Este proyecto tiene como objetivo automatizar las siguientes:
1. La gestión de los **retrasos de 1ª hora**.
2. La evolución del **semáforo de colores**.
3. El registro de los partes de conducta que llevan a la apertura de **expedientes**.

## Arquitectura
La herramienta trabaja en 4 niveles muy diferenciados.
- **Nivel 1 -  Ingesta de datos:** La herramienta se encarga de buscar y leer la hoja de cálculo donde está la base de datos original.
- **Nivel 2 - Preprocesamiento de datos:** Se limpian los datos y se llevan a un formato uniforme y fácil de manejar.
- **Nivel 3 - Análisis de datos:** Se aplican una serie de reglas para obtener unos resúmenes con la información relativa a los retrasos, colores, y expedientes.
- **Nivel 4 - Creación de informes:** Los resúmenes del nivel anterior se exportan a un documento que el usuario final pueda leer (pdf, hoja de cálculo, etc).

## Reglas
El análisis de datos del nivel 3 tiene que obtener una serie de resúmenes a partir de la base de datos. Para ello, hay que seguir las reglas que se muestran a continuación:
### Reglas de retrasos
- Cada 3 retrasos, hay que:
	- Generar una incidencia (*esto no se automatiza*).
	- Generar un documento de notificación a familias.
	- Crear registro en la base de datos para quitar el 10% de la nota de valores.
### Reglas del semáforo
- Cada 3 CFCs, se sube un color.
- Cada 3 incidencias, se baja un color.
- Cada CCC, se baja un color.
- Cada CGPC, se baja directamente al rojo (independientemente de subidas por otros motivos)
- Cada 2 semanas sin incidencias, CCCs, o CGPCs, los que están en el amarillo o en el rojo suben un color.
### Reglas de expedientes
- Cada CGPC supone un expediente automáticamente.
- Al acumular 6 CCCs, y luego cada 3 CCCs, se abre un expediente.