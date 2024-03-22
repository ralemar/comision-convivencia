from pathlib import Path

INPUTS_PATH = Path("inputs")
CHECKPOINTS_PATH = INPUTS_PATH / "checkpoints.txt"
DATES_PATH = INPUTS_PATH / "fechas.txt"
XLSX_FILEPATH = INPUTS_PATH / "data.xlsx"
PROCEEDINGS_DATE_PATH = INPUTS_PATH / "fechas_expedientes.txt"

OUTPUTS_PATH = Path("outputs")
COLORS_SUBDIR = Path("colores")
TARDIES_SUBDIR = Path("retrasos")

TMP_PATH = Path("tmp")
SRC_PATH = Path("src")
NOTIFICATION_PATH = SRC_PATH / "notificacion"

##### EXCEL USELESS TABS
EXCEL_USELESS_TABS = [
        "Instrucciones",
        "CCCEXP",
        "Retrasos 1ªh"
]

##### ORIGINAL COLUMN NAMES
ORIGINAL_COLUMN_NAME_STUDENT = "Nombre y Apellidos del alumnado al que se abre el parte:"
ORIGINAL_COLUMN_NAME_DATE_OF_RECORD = "Marca temporal"
ORIGINAL_COLUMN_NAME_DATE_OF_EVENT = "Fecha de la incidencia"
ORIGINAL_COLUMN_NAME_EVENT = "Tipo de conducta"

##### NEW COLUMN NAMES
COLUMN_NAME_STUDENT = "Estudiante"
COLUMN_NAME_DATE_OF_RECORD = "Fecha Registro"
COLUMN_NAME_DATE_OF_EVENT = "Fecha Evento"
COLUMN_NAME_EVENT = "Evento"
COLUMN_NAME_GROUP = "Grupo"

##### EXCEL VALID COLUMNS
EXCEL_VALID_COLUMNS = [
        ORIGINAL_COLUMN_NAME_DATE_OF_EVENT,
        ORIGINAL_COLUMN_NAME_STUDENT,
        ORIGINAL_COLUMN_NAME_EVENT,
        ORIGINAL_COLUMN_NAME_DATE_OF_RECORD
]

EXCEL_VALID_COLUMNS_RENAMED = [
        COLUMN_NAME_DATE_OF_EVENT,
        COLUMN_NAME_STUDENT,
        COLUMN_NAME_EVENT,
        COLUMN_NAME_DATE_OF_RECORD
]




STATE_TO_COLOR = {
    -2: "ROJO",
    -1: "AMARILLO",
    0: "VERDE",
    1: "AZUL"
}


###### STRINGS THAT DEFINE EVENTS
CFC_NAME = "CFC (Conducta favorable a la convivencia)"
INCIDENT_NAME = "Incidencia"
CCC_NAME = "CCC (Conducta contraria a la convivencia)"
CEG_NAME = "CGPC (condcutas gravemente perjudiciales para la convivencia)"
TARDY_NAME = "Retraso (1ªh)"
