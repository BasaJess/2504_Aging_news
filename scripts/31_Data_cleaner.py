# In this script we will create functions that will take the dataframe extracted from the vector database and has the date in the form of the LLM response, we need to extract the date, only the date and place it in a datetime format. 
# then save it into df, and file,  csv and json


import pandas as pd

def extract_date(date_string):
    try:
        date = pd.to_datetime(date_string, errors='coerce')
        if pd.isnull(date):
            return "Invalid date"
        return date.date()  # returns only the date part
    except Exception as e:
        return f"Error: {e}"


def clean_and_save_docs_df(df):
    """ The expected df must have the following cols: "file_name", "relevance_for_longevity", "date_of_publication", "author", "institution", "peer_reviewed","summary"

    """
    # iterate through each row and extract the string of the field "date_of_publication"
        # extract_date() function for each row in the df
        # replace the value

    # The column Peer revied has a response from the LLM, we leave that the way it is for now. It could also be simplified toa yes or no

    # Do I need to clean more? Columns or Rows?
    # The file_name is wrong, itis in float format, should be a string, he problem is that leading zeros are gone. We will have to solve that later 

    return df