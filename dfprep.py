import pandas as pd




def prepare_dataframe(url):
    """
    Load and preprocess survey data from a specified CSV URL.

    This function fetches survey data from a Google Sheets document exported as a CSV file.
    It processes the data by performing the following steps:
    - Reads the data into a pandas DataFrame.
    - Removes duplicate records based on all columns except the first one (assumed index).
    - Converts the 'Timestamp' column to datetime objects for easier manipulation and analysis.

    Returns:
        pd.DataFrame: A cleaned DataFrame with survey data ready for analysis.

    Note:
        The URL is hardcoded and points to a specific Google Sheets CSV export. Changes in the
        structure of the CSV or the URL will require updates to this function.
    """

    renamelist = ['Timestamp', 'musicartist', 'height', 'city', 'thirtymin', 'travel', \
                  'likepizza', 'deepdish', 'sport', 'spell', 'hangout', 'talk', \
                  'year', 'quote', 'areacode', 'pets', 'superpower', 'shoes']



    # create data frame from url
    df1 = pd.read_csv(url)

    # drop duplicates
    df1 = df1.drop_duplicates(subset=df1.columns[1:])

    # convert to timestamp
    df1.Timestamp = pd.to_datetime(df1.Timestamp)

    # assign original headers to list
    survey_questions = df1.columns.to_list()

    # replace with column names easier to work with
    df1.columns = renamelist

    # create dict mapping column names to original questions
    label_dict = {}
    for i in range(len(renamelist)):
        label_dict[renamelist[i]] = survey_questions[i]

    return df1, label_dict
