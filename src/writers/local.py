from pathlib import Path
import pandas as pd


#### CONSTANTS 
OUTPUTS_PATH = Path("outputs")
COLORS_SUBDIR = Path("colores")
TARDIES_SUBDIR = Path("retrasos")
PROCEEDINGS_SUBDIR = Path("expedientes")
TMP_PATH = Path("tmp")
SRC_PATH = Path("src")
NOTIFICATION_PATH = SRC_PATH / "notificacion"

STATE_TO_COLOR = {
    -2: "ROJO",
    -1: "AMARILLO",
    0: "VERDE",
    1: "AZUL"
}



def copy_temporal_files():

    # Copy template files into tmp folder
    src_filepath = NOTIFICATION_PATH / "template.typ"
    tmp_filepath = TMP_PATH / "template.typ"
    tmp_filepath.write_text(src_filepath.read_text())
    src_filepath = NOTIFICATION_PATH / "logo.jpg"
    tmp_filepath = TMP_PATH / "logo.jpg"
    tmp_filepath.write_bytes(src_filepath.read_bytes())



def make_dirs(
    meeting_date,
    tardies=False,
    colors=False,
    proceedings=False
):

    # Get all the paths
    date_string = meeting_date.strftime("%y%m%d")
    meeting_dir_path = OUTPUTS_PATH / date_string
    tardy_reports_dir_path = meeting_dir_path / TARDIES_SUBDIR
    colors_reports_dir_path = meeting_dir_path / COLORS_SUBDIR
    proceedings_reports_dir_path = meeting_dir_path / PROCEEDINGS_SUBDIR

    # Careful, this line could trigger an error if an old file is open.
    meeting_dir_path.mkdir(parents=True, exist_ok=True)
    if tardies:
        tardy_reports_dir_path.mkdir(parents=True, exist_ok=True)
    if colors:
        colors_reports_dir_path.mkdir(parents=True, exist_ok=True)
    if proceedings:
        proceedings_reports_dir_path.mkdir(parents=True, exist_ok=True)




##### TARDIES OUTPUT

def write_one_tardy_report(
        student_name=None,
        group_name=None,
        meeting_date=None,
        report_number=None,
        tardy_dates=None
):
    # CONDITIONAL IMPORT
    import typst

    # Create file name for the source code
    date_string = meeting_date.strftime("%y%m%d")
    filename = f"{date_string}-{group_name}-{student_name}-{report_number}.typ"
    input_path = TMP_PATH / filename

    # Create contents
    lines = [
        "#import \"template.typ\": template",
        "#template(",
        f"    \"{student_name}\",",
        f"    \"{group_name}\",",
        f"    \"{meeting_date.strftime('%Y-%m-%d')}\",",
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
    output_path = OUTPUTS_PATH / date_string / "retrasos" / filename
    output_path = output_path.with_suffix(".pdf")

    # Generate file with typst
    typst.compile(input_path, output=output_path)



def export_tardies(all_tardies):

    copy_temporal_files()

    if len(all_tardies) == 0:
        print("No hay retrasos!")
    else:
        # Pick the meeting date from the first entry
        meeting_date = all_tardies[0]["meeting_date"]
        make_dirs(meeting_date, tardies=True)

    for tardy_report in all_tardies:

        write_one_tardy_report(**tardy_report)



#### COLORS OUTPUT

def get_student_color_report(
    student_name=None,
    group_name=None,
    meeting_date=None,
    old_state=None,
    new_state=None,
    n_CFC_upgrades=None,
    n_incident_downgrades=None,
    n_CCC_downgrades=None,
    has_CEG=None,
    has_no_incidents_or_CCCs=None
):

    old_color = STATE_TO_COLOR[old_state]
    new_color = STATE_TO_COLOR[new_state]

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


def get_colors_and_explanation(
    old_state=None,
    new_state=None,
    n_CFC_upgrades=None,
    n_incident_downgrades=None,
    n_CCC_downgrades=None,
    has_CEG=None,
    has_no_incidents_or_CCCs=None,
    **kwargs
):

    old_color = STATE_TO_COLOR[old_state]
    new_color = STATE_TO_COLOR[new_state]

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

    return old_color, new_color, explanations


def prepare_color_explanation_for_txt(
    student_name,
    old_color,
    new_color,
    explanations
):

    if old_color == new_color:
        summary = f"{student_name} se mantiene en el {old_color}."
    else:
        summary = f"{student_name} pasa del {old_color} al {new_color}."

    # Let's format things nicely
    report = f"- {summary}\n"
    for exp in explanations:
        report = report + f"    * {exp}\n"

    return report




def export_colors_in_txt(all_colors):

    # Prepare everything
    meeting_date = all_colors[0][0]["meeting_date"]
    make_dirs(meeting_date, colors=True)

    for group_reports in all_colors:

        # Get path of report
        date_string = meeting_date.strftime("%y%m%d")
        group_name = group_reports[0]["group_name"]
        output_path = OUTPUTS_PATH / date_string / COLORS_SUBDIR / group_name
        output_path = output_path.with_suffix(".txt")

        # Add contents to report
        with open(output_path, 'w', encoding="utf8") as f:

            # Iterate over students in the group:
            for student_report in group_reports:

                old_color, new_color, explanations = get_colors_and_explanation(
                    **student_report    
                )
                new_lines = prepare_color_explanation_for_txt(
                    student_report["student_name"],
                    old_color,
                    new_color,
                    explanations
                )
                #new_lines = get_student_color_report(**student_report)
                f.write(new_lines)




def export_colors_in_excel(all_colors):

    # Prepare everything
    meeting_date = all_colors[0][0]["meeting_date"]
    make_dirs(meeting_date, colors=True)

    for group_reports in all_colors:

        # Get path of report
        date_string = meeting_date.strftime("%y%m%d")
        group_name = group_reports[0]["group_name"]
        output_path = OUTPUTS_PATH / date_string / COLORS_SUBDIR / group_name
        output_path = output_path.with_suffix(".xlsx")

        # Add contents to report
        records = []

        # Iterate over students in the group:
        for student_report in group_reports:

            old_color, new_color, explanations = get_colors_and_explanation(
                **student_report    
            )
            new_lines = prepare_color_explanation_for_txt(
                student_report["student_name"],
                old_color,
                new_color,
                explanations
            )

            record = {
                "Estudiante": student_report["student_name"],
                "Viejo color": old_color,
                "Nuevo color": new_color,
                "Explicación": explanations
            }
            records.append(record)
        df = pd.DataFrame(data=records)
        df.to_excel(output_path)


def export_colors(all_colors, mode="EXCEL"):

    if mode == "EXCEL":
        export_colors_in_excel(all_colors)
    elif mode == "txt":
        export_colors_in_txt(all_colors)
    else:
        print("MODO NO DETECTADO")





##### PROCEEDINGS

def export_proceedings(all_proceedings):

    # Prepare everything
    if len(all_proceedings) == 0:
        print("No hay CCCs ni CGPCs!")
    else:
        # Pick the meeting date from the first entry
        meeting_date = all_proceedings[0]["meeting_date"]
        make_dirs(meeting_date, proceedings=True)


    # Get path of report
    date_string = meeting_date.strftime("%y%m%d")
    output_path = OUTPUTS_PATH / date_string / PROCEEDINGS_SUBDIR / "expedientes"
    output_path = output_path.with_suffix(".xlsx")

    # Add contents to report
    df = pd.DataFrame(all_proceedings)

    # Drop some columns
    df.drop(
        columns=[
            "meeting_date", 
            "N_previous_CEGs",
            "N_previous_CCCs",
            "N_previous_CCC_proceedings",
            "N_previous_total_proceedings"
        ],
        inplace=True
    )

    df.to_excel(output_path)  