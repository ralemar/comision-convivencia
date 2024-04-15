import streamlit as st
from datetime import date

import src.readers.local as reader
import src.preprocess as pp
import src.tardies as tardies
import src.colors as colors
import src.proceedings as proceedings
import src.writers.local as writer




st.title('Comisión de convivencia')

intro_text = """
Esta herramienta automatiza hasta 3 tareas diferentes:

1. El seguimiento de los retrasos de los alumnos.
2. La evolución del semáforo de colores para cada grupo.
3. El contador de CCCs y expedientes disciplinarios.
"""

st.header("Introducción")
st.write(intro_text)



st.header("Parámetros de entrada")


uploaded_file = st.file_uploader("Elige un archivo")

all_date_strings = [
    "2023-09-01",
    "2023-09-22",
    "2023-10-06",
    "2023-10-20",
    "2023-11-03",
    "2023-11-17",
    "2023-12-08",
    "2024-12-22",
    "2024-01-19",
    "2024-02-02",
    "2024-02-23",
    "2024-03-08",
    "2024-03-22",
    "2024-04-19",
    "2024-05-03",
    "2024-05-17",
    "2024-05-31",
    "2024-06-14"
]
intervals = [
    [all_date_strings[i], all_date_strings[i+1]] 
    for i in range(len(all_date_strings) - 1)
]
interval_strings = [f"Desde el {x[0]} hasta el {x[1]}" for x in intervals]

option = st.selectbox(
    "Intervalo de estudio",
    interval_strings,
    index=None,
    placeholder="Elige un intervalo de fechas...",
)

comparison_date = st.date_input("Fecha de última revisión de expedientes")




st.header("Parámetros de salida")

analyze_tardies = st.checkbox('Analizar retrasos', value=True)
analyze_colors = st.checkbox('Analizar colores', value=True)
analyze_proceedings = st.checkbox('Analizar expedientes', value=True)



finished = False
if st.button('Comenzar análisis', type="primary"):
    
    # Nivel 1
    st.write("Leyendo datos")

    all_dates = [date.fromisoformat(x) for x in all_date_strings]
    checkpoint = interval_strings.index(option)+1
    today = date.today()
    raw_dataframes = reader.read_excel(uploaded_file)
    input_data = {
        "raw_dataframes": raw_dataframes,
        "all_dates": all_dates,
        "checkpoint": checkpoint,
        "comparison_date": comparison_date,
        "meeting_date": today,
    }

    # Nivel 2
    st.write("Preprocesando datos")
    pp.preprocess_data(input_data)

    # Nivel 3
    st.write("Analizando datos")
    if analyze_tardies:
        all_tardies = tardies.process_all_students(input_data)
    if analyze_colors:
        all_colors = colors.process_all_students(input_data)
    if analyze_proceedings:
        all_proceedings = proceedings.process_all_students(input_data)

    # Nivel 4
    st.write("Creando informes")
    if analyze_tardies:
        writer.export_tardies(all_tardies)
    if analyze_colors:
        writer.export_colors(all_colors)
    if analyze_proceedings:
        writer.export_proceedings(all_proceedings)
    writer.create_zip_file()

    finished=True


if finished:
    with open(writer.TMP_PATH / "informes.zip", "rb") as file:
        btn = st.download_button(
            label="Descargar informes",
            data=file,
            file_name="informes.zip"
        )

