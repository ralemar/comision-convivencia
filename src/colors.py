from datetime import timedelta
from . import settings as S

def get_number_of_CFC_upgrades(student_df, start_date, final_date):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.CFC_NAME)
    CFCs_df = student_df[mask]

    # Number of CFCs before the begining of the period.
    mask_1 = CFCs_df[S.COLUMN_NAME_DATE_OF_RECORD] <= start_date
    R_i = len(CFCs_df[mask_1])

    # Number of CFCs before the end of the period.
    mask_2 = CFCs_df[S.COLUMN_NAME_DATE_OF_RECORD] <= final_date
    R_f = len(CFCs_df[mask_2])

    # Number of CFCs already considered for an upgrade.
    n = R_i - (R_i % 3)

    # Number of CFCs that could grant a new upgrade.
    N = R_f - n

    # Number of upgrades.
    N_upgrades = N // 3
    return N_upgrades



def get_number_of_incident_downgrades(student_df, start_date, final_date):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.INCIDENT_NAME)
    incidents_df = student_df[mask]

    # Number of incidents before the begining of the period.
    mask_1 = incidents_df[S.COLUMN_NAME_DATE_OF_RECORD] <= start_date
    R_i = len(incidents_df[mask_1])

    # Number of incidents before the end of the period.
    mask_2 = incidents_df[S.COLUMN_NAME_DATE_OF_RECORD] <= final_date
    R_f = len(incidents_df[mask_2])

    # Number of incidents already considered for a downgrade.
    n = R_i - (R_i % 3)

    # Number of incidents that could grant a new downgrade.
    N = R_f - n

    # Number of downgrades.
    N_downgrades = N // 3
    return N_downgrades


def get_number_of_CCC_downgrades(student_df, start_date, final_date):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.CCC_NAME)
    CCCs_df = student_df[mask]

    # Number of incidents before the begining of the period.
    mask_1 = CCCs_df[S.COLUMN_NAME_DATE_OF_RECORD] <= start_date
    R_i = len(CCCs_df[mask_1])

    # Number of incidents before the end of the period.
    mask_2 = CCCs_df[S.COLUMN_NAME_DATE_OF_RECORD] <= final_date
    R_f = len(CCCs_df[mask_2])

    # Number of downgrades.
    N_downgrades = R_f - R_i
    return N_downgrades


def is_there_any_CEG(student_df, start_date, final_date):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.CEG_NAME)
    CEGs_df = student_df[mask]

    # Number of CEG within the period
    mask_1 = CEGs_df[S.COLUMN_NAME_DATE_OF_RECORD] >  start_date
    mask_2 = CEGs_df[S.COLUMN_NAME_DATE_OF_RECORD] <= final_date
    mask = mask_1 & mask_2
    N = len(CEGs_df[mask])

    if N >= 1:
        return True
    else:
        return False

def are_there_incidents_or_CCCs(student_df, start_date, final_date):

    mask_CCC = (student_df[S.COLUMN_NAME_EVENT] == S.CCC_NAME)
    mask_incident = (student_df[S.COLUMN_NAME_EVENT] == S.INCIDENT_NAME)
    mask = mask_CCC | mask_incident
    df = student_df[mask]

    # Number of CEG within the period
    mask_1 = df[S.COLUMN_NAME_DATE_OF_RECORD] >  start_date
    mask_2 = df[S.COLUMN_NAME_DATE_OF_RECORD] <= final_date
    mask = mask_1 & mask_2
    N = len(df[mask])

    if N >= 1:
        return False
    else:
        return True


def evolve(
    current_state,
    n_CFC_upgrades,
    n_incident_downgrades,
    n_CCC_downgrades,
    has_CEG,
    has_no_incidents_or_CCCs
):

    if has_CEG:
        return -2
    else:
        if has_no_incidents_or_CCCs:
            if current_state < 0:
                change = 1 + n_CFC_upgrades
            else:
                change = n_CFC_upgrades
        else:
            change = n_CFC_upgrades - n_incident_downgrades - n_CCC_downgrades

    final_state = current_state + change

    # Make sure the final state is not less than -2
    final_state = max(-2, final_state)
    # Make sure the final state is not more than 1
    final_state = min(1, final_state)

    return final_state



def process_colors(
    student_df,
    all_dates,
    checkpoint
):

    # Unpack data
    student_name = student_df[S.COLUMN_NAME_STUDENT].iloc[0]
    group_name = student_df[S.COLUMN_NAME_GROUP].iloc[0]

    # Initialize the state at 0 (green color)
    new_state = 0

    for i in range(checkpoint):

        old_state = new_state

        # Set the dates
        start_date = all_dates[i]
        final_date = all_dates[i+1]

        # Compute the changes
        n_CFC_upgrades = get_number_of_CFC_upgrades(student_df, start_date, final_date)
        n_incident_downgrades = get_number_of_incident_downgrades(student_df, start_date, final_date)
        n_CCC_downgrades = get_number_of_CCC_downgrades(student_df, start_date, final_date)
        has_CEG = is_there_any_CEG(student_df, start_date, final_date)
        has_no_incidents_or_CCCs = are_there_incidents_or_CCCs(student_df, start_date, final_date)

        # Compute the next state with those changes
        new_state = evolve(
            old_state,
            n_CFC_upgrades,
            n_incident_downgrades,
            n_CCC_downgrades,
            has_CEG,
            has_no_incidents_or_CCCs 
        )
    
    # Put it all tidy in a nice dict for reporting
    colors_info = {
        "student_name": student_name,
        "group_name": group_name,
        "notification_date": all_dates[checkpoint] + timedelta(days=1),
        "old_state": old_state,
        "new_state": new_state,
        "n_CFC_upgrades": n_CFC_upgrades,
        "n_incident_downgrades": n_incident_downgrades,
        "n_CCC_downgrades": n_CCC_downgrades,
        "has_CEG": has_CEG,
        "has_no_incidents_or_CCCs": has_no_incidents_or_CCCs,
    }

    return colors_info