# In this script we will create functions that will take the dataframe extracted from the vector database and has the date in the form of the LLM response, we need to extract the date, only the date and place it in a datetime format. 
# then save it into df, and file,  csv and json



import re
import os
import pandas as pd
from dateutil import parser
from datetime import date, datetime

def extract_date_from_text(text):
    """
    Extracts date information from a text snippet.
    Handles various formats (e.g. "April 12", "12/04/2025", "2025", "Apr 12th", etc.)

    Parameters:
    - text (str): Input string possibly containing a date.

    Returns:
    - str: Extracted date in YYYY-MM-DD format if found, else 'Today's date'.
    """
    try:
        # Use regex to find chunks that look like dates
        date_patterns = re.findall(r'\b(?:\d{1,2}[/-])?(?:\d{1,2}[/-])?\d{2,4}|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t)?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[^\n.,]*', text, flags=re.IGNORECASE)

        for chunk in date_patterns:
            try:
                parsed_date = parser.parse(chunk, fuzzy=True)
                return parsed_date.date().isoformat()  # YYYY-MM-DD
            except:
                continue

        # Fallback: try whole sentence as last resort
        parsed_date = parser.parse(text, fuzzy=True)
        return parsed_date.date().isoformat()

    except Exception:
        return str(date.today())



def clean_and_save_docs_df(df):
    """ The expected df must have the following cols: "file_name", "relevance_for_longevity", "date_of_publication", "author", "institution", "peer_reviewed","summary"
    
    """
    df = df.copy() # just in case
    
    # iterates through each row in df and extract the string of the field "date_of_publication"
        # applies extract_date_from_text(text) function for each row in the df
        # replace the value
        # Convert the 'date_of_publication' column to datetime
        # errors='coerce' ensures that if a value cannot be converted to a valid datetime, it will be replaced with NaT (Not a Time), which is pandas’ equivalent of NaN for datetime.
    df['Date_of_publication'] = df['Date_of_publication'].apply(extract_date_from_text)
    
    df['Date_of_publication'] = pd.to_datetime(df['Date_of_publication'], errors='coerce')

    df['Date_of_publication'] = df['Date_of_publication'].fillna(pd.to_datetime(datetime.today().date()))

    # The column Peer revied has a response from the LLM, we leave that the way it is for now. It could also be simplified toa yes or no

    # Do I need to clean more? Columns or Rows?
    # The file_name is wrong, it is in float format, should be a string, he problem is that leading zeros are gone. We will have to solve that later 


    df.to_csv(".." + os.sep + "data" + os.sep + "results" + os.sep + "cleaned_docs_info.csv")

    return df