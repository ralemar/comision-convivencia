from . import settings as S


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

def get_student_status(student_df):

    N_CCCs = get_number_of_CCCs(student_df)
    N_CEGs = get_number_of_CEGs(student_df)
    N_CCC_proceedings = get_number_of_CCC_proceedings(N_CCCs)

    return N_CEGs, N_CCCs, N_CCC_proceedings


def process_student(
    student_df, 
    meeting_date, 
    comparison_date=None
):

    # Get rid of posterior dates
    mask = (student_df[S.COLUMN_NAME_DATE_OF_RECORD] <= meeting_date)
    filtered_df = student_df[mask]
    proceedings_data = get_student_status(filtered_df)

    # Compare with previous data if comparison date is provided
    if comparison_date:

        mask = (student_df[S.COLUMN_NAME_DATE_OF_RECORD] < comparison_date)
        filtered_df = student_df[mask]
        previous_proceedings_data = get_student_status(filtered_df)

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




def process_all_students(
    input_data 
):

    # Unpack the required data
    meeting_date = input_data["meeting_date"]
    comparison_date = input_data["comparison_date"]
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
            proceedings_info = process_student(
                student_df,
                meeting_date,
                comparison_date
            )

            # Put it all nice and tidy for reporting

            # Is there anything to report in the first place?
            if proceedings_info["N_CCCs"] > 0 or proceedings_info["N_CEGs"] > 0:
                proceedings_report = {
                    "group_name": group_name,
                    "student_name": student_name,
                    "meeting_date": meeting_date
                }
                # Add the colors info
                proceedings_report = proceedings_report | proceedings_info
                reports.append(proceedings_report)

    return reports