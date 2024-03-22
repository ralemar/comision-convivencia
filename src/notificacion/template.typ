#let template(
    student_name,
    group_name,
    notification_date,
    tardy_date_1,
    tardy_date_2,
    tardy_date_3,
) = [

#set par(justify: true)

#grid(
    columns: (16%, auto),
    rows: 1,
    gutter: 2cm,
    image("logo.jpg", width: 100%),
    align(center + horizon)[
        = #text(
            size: 18pt,
            [AVISO AL ALUMNO/A\ POR ACUMULACIÓN DE RETRASOS]
        )
    ]
)


#v(0.5cm)

#box(
    stroke: black,
    width: 100%,
    inset: 6pt,
    [
        *Nombre y apellidos del alumno/a: #student_name* \
        *Curso: #group_name* \
        *Fecha de la notificación: #notification_date*
    ]
)

#v(0.2cm)

== Antecedentes

Este aviso se debe a la *acumulación de tres retrasos* de primera hora, los cuales tuvieron lugar en las siguientes fechas:
    - #tardy_date_1
    - #tardy_date_2
    - #tardy_date_3

#v(0.5cm)    

== Medidas adoptadas

Necesitamos mejorar la *puntualidad*, es una gran virtud que indica *responsabilidad y respeto* al resto de compañeros/as y profesores/as.

Este aviso conlleva una incidencia en el registro de convivencia y, además, la reducción del *10% de la nota de valores* de la actual evaluación.

Si continúa la acumulación de más retrasos, seguirá *reduciéndose el % de la nota de valores* y el/la alumno/a deberá realizar una medida educativa que podría conllevar una colaboración con actividades de servicio en el Instituto o actividades con el Programa Tiempo Fuera con la colaboración del ayuntamiento.


#set rect(
  inset: 8pt,
  fill: rgb("e4e5ea"),
  width: 100%,
)

#v(6cm)

#set align(center)

#grid(
  columns: (1fr, 1fr, 1fr),
  rows: 1,
  gutter: 3pt,
  [Comisión de Convivencia\ Firma:],
  [Alumno/a\ Firma:],
  [Padre/madre/tutor-a legal\ Firma:]
)

]