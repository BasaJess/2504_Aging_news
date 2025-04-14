
# Receives a cleaned df containing the info of a group of documents 
# orders the list first by relevance and then by date
# returns the list as a df 
# it organizes the returned df to be displayed later in a table in a web interface 

import pandas as pd
import os


def most_relevant_docs_list(df):
    """
    Sorts the DataFrame by relevance and date, selects the top 10,
    formats for display, and returns both the DataFrame and a JSON representation.

    Parameters:
    - df (pd.DataFrame): Cleaned DataFrame with document info.

    Returns:
    - pd.DataFrame: Sorted and formatted DataFrame (top 10 docs).
    - str: JSON string of the formatted DataFrame.
    """
    # Sort by relevance and date
    sorted_df = df.sort_values(by=['Relevance_for_longevity', 'Date_of_publication'], ascending=[False, False])


    # Select and rename columns for clean display
    display_df = sorted_df[[
        'Author', 
        'Date_of_publication', 
        'Institution', 
        'Peer Reviewed', 
        'Relevance_for_longevity', 
        'Summary'
    ]].rename(columns={
        'Date_of_publication': 'Date',
        'Peer Reviewed': 'Peer_Reviewed'
    })

    # Select top 10 rows
    top_10_df = display_df.head(10).reset_index(drop=True)

    # Convert to JSON (records = list of dicts)
    json_result = top_10_df.to_json(orient='records', force_ascii=False)

    return top_10_df, json_result


def retrieve_most_relevant_docs_for_streamlit ():
    
    df = pd.read_csv("." + os.sep + "data" + os.sep + "results" + os.sep + "cleaned_docs_info.csv")
    top_docs_df, top_docs_json = most_relevant_docs_list(df)
    return top_docs_df