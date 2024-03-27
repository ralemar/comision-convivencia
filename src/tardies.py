from . import settings as S

def get_tardies_df(student_df):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.TARDY_NAME)
    tardies_df = student_df[mask]
    return tardies_df


def get_number_of_tardy_sanctions(tardies_df, start_date, final_date):

    # Numero de retrasos anteriores a start_date
    mask_1 = tardies_df[S.COLUMN_NAME_DATE_OF_RECORD] <= start_date
    R_i = len(tardies_df[mask_1])

    # Numero de retrasos anteriores a final_date
    mask_2 = tardies_df[S.COLUMN_NAME_DATE_OF_RECORD] <= final_date
    R_f = len(tardies_df[mask_2])

    # Numero de retrasos ya fueron contados para incidencias.
    n = R_i - (R_i % 3)

    # Numero de retrasos que generan nueva incidencia
    N = R_f - n

    # Numero de incidencias
    N_sanctions = N // 3
    return N_sanctions


def get_relevant_tardy_dates(tardies_df, N_sanctions):

    # Retrieve only dates that generate the sanction
    n_dates = N_sanctions*3
    N = len(tardies_df)
    dates_to_skip = N % 3
    j = N - dates_to_skip
    i = j - n_dates
    tardy_dates = tardies_df[S.COLUMN_NAME_DATE_OF_EVENT].iloc[i:j].values
    
    return tardy_dates


def process_student(
    student_df, 
    start_date,
    final_date,
):

    # Filter only tardy instances
    tardies_df = get_tardies_df(student_df)

    # Count number of sanctions
    N_sanctions = get_number_of_tardy_sanctions(
        tardies_df,
        start_date,
        final_date
    )

    if N_sanctions > 0:
        # Extract the relevant tardy dates
        relevant_tardy_dates = get_relevant_tardy_dates(
            tardies_df,
            N_sanctions
        )
    else:
        relevant_tardy_dates = None

    # Put all the data in a nice dict
    tardy_info = {
        "N_sanctions": N_sanctions,
        "tardy_dates": relevant_tardy_dates
    }

    return tardy_info


def process_all_students(
    input_data 
):

    # Unpack the required data
    checkpoint = input_data["checkpoint"]
    start_date = input_data["all_dates"][checkpoint-1]
    final_date = input_data["all_dates"][checkpoint]
    meeting_date = input_data["meeting_date"]
    dfs = input_data["group_dfs"]

    # Prepare list that will hold all the tardies
    reports = []


    # Iterate over the groups
    for group_name, group_df in dfs.items():

        print("-"*60)
        print(f"Analizando {group_name}")

        student_names = group_df["Estudiante"].unique()

        for student_name in student_names:

            # Filter by the student name
            mask = (group_df["Estudiante"] == student_name)
            student_df = group_df.loc[mask]

            # Do the processing
            tardy_info = process_student(
                student_df,
                start_date,
                final_date
            )

            # Put it all nice and tidy for reporting, splitting by sanctions
            for i in range(tardy_info["N_sanctions"]):
                filtered_tardy_dates = tardy_info["tardy_dates"][3*i:3*i+3]
                tardy_report = {
                    "student_name": student_name,
                    "group_name": group_name,
                    "meeting_date": meeting_date,
                    "report_number": i+1,
                    "tardy_dates": filtered_tardy_dates
                }
                reports.append(tardy_report)

    return reports