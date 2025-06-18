# core/sql_validator.py

import sqlglot
from sqlglot.errors import ParseError
from sqlglot.expressions import Insert, Delete, Drop, Update

def validate_sql(sql_query: str, allow_dml: bool = False):
    try:
        parsed = sqlglot.parse_one(sql_query)

        # Block INSERT, DELETE, DROP, UPDATE if not allowed
        if not allow_dml and isinstance(parsed, (Insert, Delete, Drop, Update)):
            return {
                "valid": False,
                "error": f"DML operation '{type(parsed).__name__}' is not allowed."
            }

        return {"valid": True, "error": None}
    
    except Exception as e:
        return {"valid": False, "error": str(e)}