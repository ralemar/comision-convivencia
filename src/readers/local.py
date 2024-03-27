from pathlib import Path
from datetime import date
import pandas as pd
import csv
from .. import settings as S

INPUTS_PATH = Path("inputs")
CHECKPOINTS_PATH = INPUTS_PATH / "checkpoints.txt"
DATES_PATH = INPUTS_PATH / "fechas.txt"
XLSX_FILEPATH = INPUTS_PATH / "data.xlsx"
PROCEEDINGS_DATE_PATH = INPUTS_PATH / "fecha_comparacion.txt"
MEETING_DATE_PATH = INPUTS_PATH / "fecha_reunion.txt"




def read_excel():

    # Load the whole file into memory
    xlsx_file = pd.ExcelFile(XLSX_FILEPATH)

    # Therefore the valid tabs are as follows
    valid_tabs = []
    for tab in xlsx_file.sheet_names:
        if tab not in S.SHEET_USELESS_TABS:
            valid_tabs.append(tab)

    # Read the valid tabs with the valid columns only
    raw_dataframes = pd.read_excel(
        xlsx_file,
        header = 0,
        sheet_name = valid_tabs,
        usecols = S.SHEET_VALID_COLUMNS,
    )

    return raw_dataframes


def read_meeting_date():

    with open(MEETING_DATE_PATH, 'r', encoding="utf8") as file:
        date_string = file.read()
        return date.fromisoformat(date_string)


def read_all_dates():

    with open(DATES_PATH, 'r', encoding="utf8", newline="") as file:

        reader = csv.reader(file, delimiter=',')
        next(reader) # skip header row
        all_dates = []
        for (index, date_string) in reader:
            all_dates.append(date.fromisoformat(date_string.strip()))
        return all_dates


def read_comparison_date():

    with open(PROCEEDINGS_DATE_PATH, 'r', encoding="utf8") as file:
        date_string = file.read()
        if date_string == "None":
            return None
        else:
            return date.fromisoformat(date_string)


def read_checkpoint():

    with open(CHECKPOINTS_PATH, 'r', encoding="utf8") as file:
        checkpoint = int(file.read())
    if checkpoint == 0:
        print("El checkpoint debería ser positivo, no 0.")
    return checkpoint



def read_data():

    # Load all the data
    raw_dataframes = read_excel()
    all_dates = read_all_dates()
    checkpoint = read_checkpoint()
    comparison_date = read_comparison_date()
    meeting_date = read_meeting_date()

    raw_data = {
        "raw_dataframes": raw_dataframes,
        "all_dates": all_dates,
        "checkpoint": checkpoint,
        "comparison_date": comparison_date,
        "meeting_date": meeting_date,
    }

    return raw_data