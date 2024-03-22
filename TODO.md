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

- Preparar repositorio
    + gitignore
    + push a github para poder clonar
- Implementar readers y writers

- Empaquetar en git para que sea importable desde Colab.
- Preparar secuencia de comandos para Colab.
- Experimentar con zapier y los triggers...


- Separar constantes lógicas y constantes de IO?
- Implementar Objetos para no pasar mil variables
    - Las funciones que reciben el dict con tardy_info o color_info deberían esperar argumentos normales. Si acaso, debería pasarlos yo explícitamente, tal vez ahorrando haciendo un unpacking de una named tuple.
    - Resolver incoherencia de fechas, pasarlas por fuera, calcularlas dentro, calcular a mano notification date todo el rato...
    - Abrir los archivos 1 vez al inicializar el objeto, mucho más rápido.

- Idea: introducir un log donde se muestren algunos resumenes para verificar que no se ha liado, rollo... detectados estos grupos, con tantos eventos por grupo.
- Configurar verbosidad
- Meter rich text

- Hacer script que calcule retrasos, colores, expedientes por separado. Meter fecha como parámetro? Que se calcule automáticamente si no se da...
- En COLAB, la salida de retrasos meterla al excel de origen...
- Contemplar absentistas.
- Cambiar nombre funciones CEG: 

- Corregir errata en las CCC muy graves, en fuente y en código.