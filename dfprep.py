import pandas as pd

renamelist = ['Timestamp', 'musicartist', 'height', 'city', 'thirtymin', 'travel', \
              'likepizza', 'deepdish', 'sport', 'spell', 'hangout', 'talk', \
              'year', 'quote', 'areacode', 'pets', 'superpower', 'shoes']


def get_data(url=None):
    try:
        if url:
            df1 = pd.read_csv(url, header=0)
            df1.to_csv("data/surveydata.csv", index=False)
        else:
            df1 = pd.read_csv("data/surveydata.csv", header = 0)

    except Exception as e:
        raise Exception(f"Failed to load data: {e}")
    return df1


def prepare_dataframe(df1, renamelist):
    # Ensure the rename list matches the dataframe column count
    if len(renamelist) != len(df1.columns):
        raise ValueError("The number of elements in 'renamelist' must match the number of columns in the dataframe.")

    # Drop duplicates considering all columns but the first (usually ID or Timestamp)
    df1 = df1.drop_duplicates(subset=df1.columns[1:])

    # Convert 'Timestamp' column to datetime format assuming 'Timestamp' is correctly positioned in renamelist
    df1.loc[:, renamelist[0]] = pd.to_datetime(df1.iloc[:, 0])

    # Map new column names
    original_columns = df1.columns.tolist()
    df1.columns = renamelist

    # Create a dictionary mapping new column names to original questions
    label_dict = dict(zip(renamelist, original_columns))

    return df1, label_dict