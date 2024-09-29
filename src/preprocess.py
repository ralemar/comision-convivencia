from . import settings as S
import numpy as np
import dateutil.parser as parser
from datetime import date

def preprocess_tab(df, group_name):

    # Get rid of all the initial empty rows AND the repeated headers row
    mask = df[S.ORIGINAL_COLUMN_NAME_DATE_OF_EVENT] == S.ORIGINAL_COLUMN_NAME_DATE_OF_EVENT
    n = df[mask].index[0]
    n = n+1 # For the repeated headers row
    df = df.iloc[n:]
    df.reset_index(drop=True, inplace=True)

    # Rename the dataframe with more convenient names
    mapper = dict(zip(S.SHEET_VALID_COLUMNS, S.SHEET_VALID_COLUMNS_RENAMED))
    df = df.rename(columns=mapper)

    # Get rid of other empty rows
    # But first convert to NaN (Excel does this, google sheets does not)
    df['Fecha Evento'] = df['Fecha Evento'].replace('', np.nan)
    df = df.dropna()

    # Reorder the columns so that they are in the specified order
    df = df[S.SHEET_VALID_COLUMNS_RENAMED]

    # Convert datetime objects to date (without the time)
    df[S.COLUMN_NAME_DATE_OF_EVENT] = [
        parser.parse(ds, dayfirst=True).date() for ds in df[S.COLUMN_NAME_DATE_OF_EVENT]
    ]

    df[S.COLUMN_NAME_DATE_OF_RECORD] = [
        parser.parse(ds, dayfirst=True).date() for ds in df[S.COLUMN_NAME_DATE_OF_RECORD]
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


def process_all_date_strings(all_date_strings):

    # Convert from strings to date object
    processed_dates = [date.fromisoformat(x) for x in all_date_strings]
    
    # Get intervals with elements k,k+1 of list and the text that will be displayed
    intervals = [
        [all_date_strings[i], all_date_strings[i+1]] 
        for i in range(len(all_date_strings) - 1)
    ]
    interval_strings = [f"Desde el {x[0]} hasta el {x[1]}" for x in intervals]

    # Find how many intevarls have passed
    today = date.today()
    for i, d in enumerate(processed_dates[1:]):
        if today < d:
            break 

    # If the first interval is not over yet, take it anyway
    if i == 0:
        i = 1

    return processed_dates, interval_strings, i