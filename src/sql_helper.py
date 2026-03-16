import pandas as pd

def run_sql(query: str, connection):
    """Execute a SELECT query and return rows as a list of dicts."""
    try:
        result = pd.read_sql_query(query, connection)
        return result.to_dict(orient="records")
    except Exception as e:
        return [{"error": str(e)}]