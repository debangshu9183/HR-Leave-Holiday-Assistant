import pandas as pd
import sqlite3

def load_csv_to_db(csv_path: str):

# Read CSV safely
    df=pd.read_csv(csv_path, encoding="latin-1", engine="python")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    # Rename problematic SQL keywords
    df.rename(columns={
        "From": "start_date",
        "To": "end_date"
    }, inplace=True)

    # Convert date columns properly (DD-MM-YYYY → datetime)
    df["start_date"] = pd.to_datetime(df["start_date"], dayfirst=True, errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], dayfirst=True, errors="coerce")

    # Create SQLite database in memory
    connection = sqlite3.connect(":memory:")

    # Insert dataframe into SQL table
    df.to_sql("holidays", connection, if_exists="replace", index=False)

    return df, connection
