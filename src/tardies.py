from . import settings as S
from datetime import timedelta

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
    tardy_dates = tardies_df[S.COLUMN_NAME_DATE_OF_EVENT].iloc[-n_dates:].values
    return tardy_dates


def process_tardies(
    student_df, 
    start_date,
    final_date    
):

    # Unpack data
    student_name = student_df[S.COLUMN_NAME_STUDENT].iloc[0]
    group_name = student_df[S.COLUMN_NAME_GROUP].iloc[0]
    notification_date = final_date + timedelta(days=1)

    # Filter only tardy instances
    tardies_df = get_tardies_df(student_df)

    # Count number of sanctions
    N_sanctions = get_number_of_tardy_sanctions(
        tardies_df,
        start_date,
        final_date
    )

    # Extract the relevant tardy dates
    relevant_tardy_dates = get_relevant_tardy_dates(
        tardies_df,
        N_sanctions
    )

    # Put all the data in a nice dict
    tardy_info = {
        "student_name": student_name,
        "group_name": group_name,
        "N_sanctions": N_sanctions,
        "notification_date": notification_date,
        "tardy_dates": relevant_tardy_dates
    }

    return tardy_info