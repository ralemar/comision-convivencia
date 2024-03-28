from google.colab import auth
from google.auth import default
import gspread
import pandas as pd
from .. import settings as S
from datetime import date


def read_data(
    limites_de_ventanas=None,
    ventana_a_estudiar=None,
    fecha_reunion=None,
    fecha_comparacion_expedientes=None,
    document_key=None
):

    # Connect to your google account
    auth.authenticate_user()
    creds, _ = default()
    gc = gspread.authorize(creds)

    # Open the worksheet
    key = "15YRMYwCh-f_hWE4vM26k3zf4Fdlpd9y4B0ugC1nlwNU"
    sheet = gc.open_by_key(key)
    worksheets = sheet.worksheets()

    # Extract the valid tab names
    valid_tabs = []
    for i, worksheet in enumerate(worksheets):
        if worksheet.title not in S.SHEET_USELESS_TABS:
            valid_tabs.append(worksheet.title)

    # Read the valid tabs
    raw_dataframes = {}
    for group_name in valid_tabs:
        print(f"Leyendo {group_name}")
        worksheet = sheet.worksheet(group_name) # Elige la pestaña
        df = pd.DataFrame(worksheet.get_all_records()) # Convierte en DataFrame
        df = df[S.SHEET_VALID_COLUMNS] # Filtra columnas
        raw_dataframes[group_name] = df # Guarda la tabla


    # Convert the data to the desired format
    all_dates = [date.fromisoformat(x[1]) for x in limites_de_ventanas]
    meeting_date = date.fromisoformat(fecha_reunion)
    comparison_date = date.fromisoformat(fecha_comparacion_expedientes)
    checkpoint = ventana_a_estudiar


    # Put everything into a nice dict
    input_data = {
        "raw_dataframes": raw_dataframes,
        "all_dates": all_dates,
        "meeting_date": meeting_date,
        "comparison_date": comparison_date,
        "checkpoint": checkpoint,
    }

    return input_data