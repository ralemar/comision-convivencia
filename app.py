import streamlit as st
from datetime import date

import src.readers.local as reader
import src.preprocess as pp
import src.tardies as tardies
import src.colors as colors
import src.proceedings as proceedings


# Read data from public spreadsheet to build the site
all_date_strings = reader.read_dates_from_public_spreadsheet()
all_dates, interval_strings, i = pp.process_all_date_strings(all_date_strings)



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

option = st.selectbox(
    "Intervalo de estudio",
    interval_strings,
    index=i-1,
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
    import src.writers.local as writer
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

