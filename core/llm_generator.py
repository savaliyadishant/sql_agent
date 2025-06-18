# core/llm_generator.py

from google import genai
import re
import pandas as pd
import os
# Initialize Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def clean_sql(text):
    text = re.sub(r"```(?:sql)?\s*([\s\S]*?)\s*```", r"\1", text)
    text = re.sub(r"(?m)^\s*(sqlite|ite|sql|SQL)\s*>\s*", "", text)
    text = re.sub(r"(?m)^\s*(ite)\s*$", "", text)
    lines = text.splitlines()
    sql_lines = [line for line in lines if not re.match(r"^\s*(ite|sqlite|sql|SQL)\s*$", line)]
    sql_only = "\n".join(sql_lines)
    return sql_only.strip()

def load_prompt_template():
    path = "config/prompt_template.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Generate an SQL query based on the user input: {query} and role: {role} using schema: {schema}"

def load_schema_string():
    schema_path = "config/schema.json"
    if os.path.exists(schema_path):
        import json
        with open(schema_path, "r") as f:
            schema = json.load(f)
            return json.dumps(schema, indent=2)
    return "Schema not available."

def generate_sql(user_query: str, role: str):
    template = load_prompt_template()
    schema = load_schema_string()
    filled_prompt = template.replace("{query}", user_query)\
                            .replace("{role}", role)\
                            .replace("{schema}", schema)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=filled_prompt
    )
    raw_sql = response.text.strip()
    return clean_sql(raw_sql)

def generate_natural_response(user_query: str, result_df: pd.DataFrame) -> str:
    table_text = result_df.to_csv(index=False)
    prompt = f"""
    User question: {user_query}
    SQL result:
    {table_text}
    Please answer the user's question in natural language based on this result.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    return response.text

