from . import settings as S
from datetime import timedelta


def get_number_of_CCCs(student_df):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.CCC_NAME)
    N = len(student_df[mask])

    return N

def get_number_of_CEGs(student_df):

    mask = (student_df[S.COLUMN_NAME_EVENT] == S.CEG_NAME)
    N = len(student_df[mask])

    return N


def get_number_of_CCC_proceedings(number_of_CCCs):

    if number_of_CCCs < 6:
        return 0
    else:
        return 1 + (number_of_CCCs - 6)//3

def get_proceedings(student_df):

    N_CCCs = get_number_of_CCCs(student_df)
    N_CEGs = get_number_of_CEGs(student_df)
    N_CCC_proceedings = get_number_of_CCC_proceedings(N_CCCs)

    return N_CEGs, N_CCCs, N_CCC_proceedings


def process_proceedings(
    student_df, 
    review_date, 
    comparison_date
):

    # Unpack data
    student_name = student_df[S.COLUMN_NAME_STUDENT].iloc[0]
    group_name = student_df[S.COLUMN_NAME_GROUP].iloc[0]

    # Get rid of posterior dates
    mask = (student_df[S.COLUMN_NAME_DATE_OF_RECORD] < review_date)
    filtered_df = student_df[mask]
    proceedings_data = get_proceedings(filtered_df)

    # Compare with previous data if comparison date is provided
    if comparison_date:

        mask = (student_df[S.COLUMN_NAME_DATE_OF_RECORD] < comparison_date)
        filtered_df = student_df[mask]
        previous_proceedings_data = get_proceedings(filtered_df)

        if previous_proceedings_data == proceedings_data:
            needs_update = False
        else:
            needs_update = True

    # Should we open a new proceeding if the student had an additional CCC?
    N_CCCs = proceedings_data[1]
    N_CCC_proceedings = proceedings_data[2]
    if get_number_of_CCC_proceedings(N_CCCs+1) == N_CCC_proceedings:
        issue_warning = False
    else:
        issue_warning = True

    # Put it all tidy in a nice dict for reporting
    proceedings_info = {
        "student_name": student_name,
        "group_name": group_name,
        "review_date": review_date,
        "N_CEGs": proceedings_data[0],
        "N_CCCs": proceedings_data[1],
        "N_CCC_proceedings": proceedings_data[2],
        "N_total_proceedings": proceedings_data[0] + proceedings_data[2],
        "issue_warning": issue_warning
    }

    if comparison_date:
        proceedings_info["needs_update"] = needs_update
        proceedings_info["N_previous_CEGs"] = previous_proceedings_data[0]
        proceedings_info["N_previous_CCCs"] = previous_proceedings_data[1]
        proceedings_info["N_previous_CCC_proceedings"] = previous_proceedings_data[2]
        proceedings_info["N_previous_total_proceedings"] = previous_proceedings_data[0] + previous_proceedings_data[2]

    return proceedings_info