from . import settings as S
from datetime import datetime

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
    mapper = dict(zip(S.SHEET_VALID_COLUMNS, S.SHEET_VALID_COLUMNS_RENAMED))
    df = df.rename(columns=mapper)

    # Reorder the columns so that they are in the specified order
    df = df[S.SHEET_VALID_COLUMNS_RENAMED]

    # Convert datetime objects to date (without the time)
    format_str = '%d/%m/%Y'
    df[S.COLUMN_NAME_DATE_OF_EVENT] = [
        datetime.strptime(ds, format_str).date() for ds in df[S.COLUMN_NAME_DATE_OF_EVENT]
    ]
    df[S.COLUMN_NAME_DATE_OF_RECORD] = [
        datetime.strptime(ds, format_str).date() for ds in df[S.COLUMN_NAME_DATE_OF_RECORD]
    ]

    # Add a column with the group name
    df[S.COLUMN_NAME_GROUP] = group_name

    # Reorder everything by name, then by date
    df = df.sort_values([S.COLUMN_NAME_STUDENT, S.COLUMN_NAME_DATE_OF_RECORD])

    return df



def preprocess_data(data_dict):

    # Put the preprocessed dataframes into a nice dict
    dfs = data_dict["raw_dataframes"]
    new_dfs = {
        gn: preprocess_tab(tab, gn) for (gn, tab) in dfs.items()
    }
    data_dict["group_dfs"] = new_dfs