- DONE. Quitar lectura de grupos para que el sistema sea robusto ante adición de nuveos alumnos?
- DONE. Probar si leer todas las hojas de golpe mejora la eficiencia
- DONE. Inicializar retrasos
- DONE. cambiar directorio a fecha/retrasos
- DONE. crear listado de fechas, necesario para el semáforo
- DONE. dates_dict debería ser lista pues ya va bien indexada
- DONE. Sacar la escritura de archivos a otro sitio para controlar IO sin redundancia
- DONE. Homogeneizar idioma
- DONE. Valorar sobre qué columna de fecha usar con Luis.
- CANCELED Implementar Pijul
- DONE. Valorar si puedo deshacerme de relevant dates y dejar solo dates y el checkpoint. En los colores tengo que usar start_date y final_date con distinto significado...
- DONE. Preguntar a Luis sobre casos de CEG + alcanzar 3 CFCs.
- DONE. Dejar de pasar student name y group name porque van en el dataframe o porque directamente yo lo he puesto ahí.
- DONE. preprocesar ordenar alfabeticamente
- DONE. Explicar la necesidad de imponer CEG como medida nueva.
- DONE. Hay retrasos de diferentes días registrados en la misma fecha. Debo usar las dos columnas. Una para encontrar el registro, la otra para crear el informe.
- DONE. Para los colores, Meter en un dict el estado previo, el nuevo, y todos los conceptos de subidas bajadas y devolver ese dict en la función. Con eso escribiremos algún archivo de salida por grupo.
- CANCELED: Para calcular cosas, filtrar primero df por fecha y luego por evento, MUCHO MÁS EFICIENTE, tal vez incluso oneliners... Update: No tiene sentido porque necesito saber retrasos acumulados previamente. Although una solución sería llevar un contador módulo 3... Uf. Pereza.
- DONE: Hacer que las constantes vayan en un archivo aparte. 
- DONE: borrar archivos temporales
- DONE: Añadir explicación a los amarillo rojos que no avanzan por no estar limpios de incidencias o cccs
- DONE: Dar aviso de CCCs cercana a expedientes.
- DONE: Mirar python anywhere para el hosting o GOOGLE COLAB
- DONE:Incluir en documentación que cuando uno tiene una CEG, da igual que suba de color por 3 CFCs.
- DONE: SI alguien llega tarde y pasa de 4 a 7 retrasos, los relevantes son el 4,5,6... está bien así?
- DONE: Preparar repositorio
- DONE: Separar constantes lógicas y constantes de IO
- DONE: Implementar diccionarios para no pasar mil variables
- DONE: Resolver incoherencia de fechas, pasarlas por fuera, calcularlas dentro, calcular a mano notification date todo el rato...
- DONE: Abrir los archivos 1 vez al inicializar el objeto, mucho más rápido.
- DONE: Encapsular readers y writers
- CANCELED: Contemplar absentistas. No se puede, que lo haga el profe a mano.
- DONE: cambiar proceeding dates para que sea meeting date por defecto, la de comparara leerla aparte.
- CANCELED: Hacer script que calcule retrasos, colores, expedientes por separado. (Esto ya está tan encapsulado que básicamente está hecho) Meter fecha como parámetro? Que se calcule automáticamente si no se da... (Esto no tiene sentido)
- DONE: añadir modo excel para output local








- push a github para poder clonar
- Preparar secuencia de comandos para Colab.
- Experimentar con zapier y los triggers...


- Idea: introducir un log donde se muestren algunos resumenes para verificar que no se ha liado, rollo... detectados estos grupos, con tantos eventos por grupo.
- Configurar verbosidad
- Meter salida rich text

- En COLAB, la salida de retrasos meterla al excel de origen en una pestaña nueva que dispare a zapier...

- Corregir errata en las CCC muy graves, en fuente y en código.
- Ordenar alfabéticamente NO desde el principio, solamente en el informe final de lo que sea.
- Leer todas las fechas y otras historias de un único archivo de configuracion
- export en excel para retrasos en la última pestaña del excel (o colab). Es decir, añadir output de retrasos para logear las sanciones.
- repensar jerarquía de directorios para writers, es decir, repensar que writers quiero y como llamarlos (modo consola, ficheros, excel, colab...)
- En el output de proceedings, cambiar nombre de columnas, añadir datos viejos, y calcular nuevos expedientes
- Exportar colores con excel formateado


- RENAME: nombre funciones CEG: 
- Rename checkpoint a window o interval