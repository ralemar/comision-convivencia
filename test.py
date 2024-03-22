import src.initialize as initialize
import src.tardies as tardies
import src.io as io
import src.colors as colors
import src.proceedings as proceedings

# Load the data
initialization_data = initialize.load_data()

# Make it easy to access:
dfs = initialization_data[0]
all_dates = initialization_data[1]
checkpoint = initialization_data[2]
proceeding_dates = initialization_data[3]

print(proceeding_dates)


# Iterate over the groups
for group_name, group_df in dfs.items():

    print("-"*60)
    print(f"Analizando {group_name}")

    student_names = group_df["Estudiante"].unique()

    for student_name in student_names:

        # Filter by the student name
        mask = (group_df["Estudiante"] == student_name)
        student_df = group_df.loc[mask]

        ################# Process proceedings

        # Do the processing
        proceedings_info = proceedings.process_proceedings(
            student_df,
            *proceeding_dates
        )

        #if proceedings_info["N_CCCs"] > 0 or proceedings_info["N_CEGs"] > 0:
        if proceedings_info["needs_update"]:
            print(
                proceedings_info["student_name"],
                proceedings_info["N_CEGs"],
                proceedings_info["N_CCCs"],
                proceedings_info["N_CCC_proceedings"],
                proceedings_info["N_total_proceedings"],
                proceedings_info["issue_warning"],
            )
            if proceeding_dates[1]:
                print(
                    " | ",
                    proceedings_info["needs_update"],
                    proceedings_info["N_previous_CEGs"],
                    proceedings_info["N_previous_CCCs"],
                    proceedings_info["N_previous_CCC_proceedings"],
                    proceedings_info["N_previous_total_proceedings"],
                )