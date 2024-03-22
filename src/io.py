from . import settings as S
import pandas as pd
import csv
from datetime import date
import typst


def preprocess_tab(df, group_name):

    # Get rid of all the initial empty rows AND the repeated headers row
    mask = df[S.ORIGINAL_COLUMN_NAME_DATE_OF_EVENT] == S.ORIGINAL_COLUMN_NAME_DATE_OF_EVENT
    n = df[mask].index[0]
    n = n+1 # For the repeated headers row
    df = df.iloc[n:]
    df.reset_index(drop=True, inplace=True)

    # Get rid of other empty rows
    df = df.dropna()

    # Rename the dataframe with more convenient names
    mapper = dict(zip(S.EXCEL_VALID_COLUMNS, S.EXCEL_VALID_COLUMNS_RENAMED))
    df = df.rename(columns=mapper)

    # Reorder the columns so that they are in the specified order
    df = df[S.EXCEL_VALID_COLUMNS_RENAMED]

    # Convert datetime objects to date (without the time)
    df[S.COLUMN_NAME_DATE_OF_EVENT] = [dt.date() for dt in df[S.COLUMN_NAME_DATE_OF_EVENT]]
    df[S.COLUMN_NAME_DATE_OF_RECORD] = [dt.date() for dt in df[S.COLUMN_NAME_DATE_OF_RECORD]]

    # Add a column with the group name
    df[S.COLUMN_NAME_GROUP] = group_name

    # Reorder everything by name, then by date
    df = df.sort_values([S.COLUMN_NAME_STUDENT, S.COLUMN_NAME_DATE_OF_RECORD])


    return df


def load_all_dfs():

    # Load the whole file into memory
    xlsx_file = pd.ExcelFile(S.XLSX_FILEPATH)

    # Therefore the valid tabs are as follows
    valid_tabs = []
    for tab in xlsx_file.sheet_names:
        if tab not in S.EXCEL_USELESS_TABS:
            valid_tabs.append(tab)

    # Read the valid tabs with the valid columns only
    dfs = pd.read_excel(
        xlsx_file,
        header = 0,
        sheet_name = valid_tabs,
        usecols = S.EXCEL_VALID_COLUMNS,
    )

    # Put the preprocessed dataframes into a nice dict
    new_dfs = {gn: preprocess_tab(tab, gn) for (gn, tab) in dfs.items()}
    
    return new_dfs


def read_all_dates():

    with open(S.DATES_PATH, 'r', encoding="utf8", newline="") as file:

        reader = csv.reader(file, delimiter=',')
        next(reader) # skip header row
        all_dates = []
        for (index, date_string) in reader:
            all_dates.append(date.fromisoformat(date_string.strip()))
        return all_dates


def read_proceeding_dates():

    with open(S.PROCEEDINGS_DATE_PATH, 'r', encoding="utf8", newline="") as file:
        date_strings = file.read().split(",")
        review_date = date.fromisoformat(date_strings[0])
        if len(date_strings) == 2:
            comparison_date = date.fromisoformat(date_strings[1].strip())
        else:
            comparison_date = None
        return review_date, comparison_date

def read_checkpoint():

    with open(S.CHECKPOINTS_PATH, 'r', encoding="utf8") as file:
        checkpoint = int(file.read())
    if checkpoint == 0:
        print("El checkpoint debería ser positivo, no 0.")
    return checkpoint



def create_tardy_reports(tardy_info):

    # Unpack data
    student_name = tardy_info["student_name"]
    group_name = tardy_info["group_name"]
    N_sanctions = tardy_info["N_sanctions"]
    notification_date = tardy_info["notification_date"]
    tardy_dates = tardy_info["tardy_dates"]

    # Iterate over reports
    if N_sanctions > 0:

        # Create typst file
        for i in range(N_sanctions):
            filtered_tardy_dates = tardy_dates[3*i:3*i+3]
            write_one_tardy_report(
                student_name,
                group_name,
                notification_date,
                i,
                filtered_tardy_dates
            )




def write_one_tardy_report(
        student_name,
        group_name,
        notification_date,
        notification_number,
        tardy_dates
):
    
    # Create file name for the source code
    formatted_date = notification_date.strftime("%y%m%d")
    filename = f"{formatted_date}-{group_name}-{student_name}-{notification_number}.typ"
    input_path = S.TMP_PATH / filename

    # Create contents
    lines = [
        "#import \"template.typ\": template",
        "#template(",
        f"    \"{student_name}\",",
        f"    \"{group_name}\",",
        f"    \"{notification_date.strftime('%Y-%m-%d')}\",",
        f"    \"{tardy_dates[0].strftime('%Y-%m-%d')}\",",
        f"    \"{tardy_dates[1].strftime('%Y-%m-%d')}\",",
        f"    \"{tardy_dates[2].strftime('%Y-%m-%d')}\",",
        ")"        
    ]

    # Write contents to temp file
    with open(input_path, 'wt', encoding="utf8") as f:
        for line in lines:
            f.write(f"{line}\n")

    # Get path for pdf file
    output_path = S.OUTPUTS_PATH / formatted_date / "retrasos" / filename
    output_path = output_path.with_suffix(".pdf")

    # Generate file with typst
    typst.compile(input_path, output=output_path)




def update_colors_report(colors_info):

    # Unpack data
    student_name = colors_info["student_name"]
    group_name = colors_info["group_name"]
    notification_date = colors_info["notification_date"]

    # Obtain line to add to the file
    new_lines = get_student_color_report(colors_info)

    # Get path of report
    formatted_date = notification_date.strftime("%y%m%d")
    output_path = S.OUTPUTS_PATH / formatted_date / S.COLORS_SUBDIR / group_name
    output_path = output_path.with_suffix(".txt")

    # Add contents to report
    with open(output_path, 'at', encoding="utf8") as f:
        f.write(new_lines)





def get_student_color_report(colors_info):

    # Unpack data
    student_name = colors_info["student_name"]
    group_name = colors_info["group_name"]
    notification_date = colors_info["notification_date"]
    old_state = colors_info["old_state"]
    new_state = colors_info["new_state"]
    n_CFC_upgrades = colors_info["n_CFC_upgrades"]
    n_incident_downgrades = colors_info["n_incident_downgrades"]
    n_CCC_downgrades = colors_info["n_CCC_downgrades"]
    has_CEG = colors_info["has_CEG"]
    has_no_incidents_or_CCCs = colors_info["has_no_incidents_or_CCCs"]

    old_color = S.STATE_TO_COLOR[old_state]
    new_color = S.STATE_TO_COLOR[new_state]

    if old_state == new_state:
        summary = f"{student_name} se mantiene en el {old_color}."
    else:
        summary = f"{student_name} pasa del {old_color} al {new_color}."

    if has_CEG:
        explanations = ["Pasa directamente al rojo por expediente directo."]
    else:
        explanations = []
        if n_CFC_upgrades > 0:
            exp = f"Sube {n_CFC_upgrades} color por acumulación de CFCs."
            explanations.append(exp)
        if n_incident_downgrades > 0:
            exp = f"Baja {n_incident_downgrades} color por acumulación de incidencias."
            explanations.append(exp)
        if n_CCC_downgrades > 0:
            exp = f"Baja {n_CCC_downgrades} color por CCC."
            explanations.append(exp)
        if old_state < 0:
            if has_no_incidents_or_CCCs:
                exp = f"Recupera un color por no tener incidencias ni CCCs."
            else:
                exp = "No recupera color por tener alguna incidencia o CCC."
            explanations.append(exp)

    # Let's format things nicely
    report = f"- {summary}\n"
    for exp in explanations:
        report = report + f"    * {exp}\n"

    return report


        