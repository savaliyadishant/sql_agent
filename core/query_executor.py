import sqlite3
import os
from datetime import datetime
import pandas as pd

def log_executed_query(sql_query, selected_db,user_query,role):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "database": selected_db,
        "sql_query": sql_query,
        "user_query":user_query,
        "role":role
    }
    log_file = "utils/executed_query_log.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    log_df = pd.DataFrame([log_entry])
    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        log_df.to_csv(log_file, index=False)

def execute_query(sql_query, selected_db,user_query,role):
    try:
        db_filename = {
            "Sample": "sample_db.sqlite",
            "Inventory": "sample_db2.sqlite"
        }.get(selected_db)

        if not db_filename:
            raise ValueError(f"No database file found for: {selected_db}")

        db_path = os.path.join("data", db_filename)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(sql_query)

        # Check if it's a SELECT query
        if sql_query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
        else:
            conn.commit()  # Important for DML
            rows = None
            col_names = None

        conn.close()

        # Log only if query execution succeeds
        log_executed_query(sql_query, selected_db,user_query,role)

        return {"columns": col_names, "rows": rows, "error": None}

    except Exception as e:
        return {"columns": None, "rows": None, "error": str(e)}
