import json
import os

def load_schema(selected_db: str):
    schema_filename = f"config/schema_{selected_db.lower()}.json"
    if os.path.exists(schema_filename):
        with open(schema_filename, "r") as f:
            return json.load(f)
    else:
        print(f"⚠️ Schema file not found: {schema_filename}")
        return {"tables": [], "database": selected_db}

def format_schema_for_prompt(schema_json):
    formatted = ""
    for table in schema_json["tables"]:
        formatted += f"Table `{table['name']}`:\n"
        for col in table["columns"]:
            col_def = f"  - {col['name']} ({col['type']})"
            if "key" in col:
                col_def += f" [{col['key']}]"
            if "foreign_key" in col:
                col_def += f" [FK -> {col['foreign_key']}]"
            formatted += col_def + "\n"
        formatted += "\n"
    return formatted

def build_prompt(user_query, role, selected_db):
    schema = load_schema(selected_db)
    schema_text = format_schema_for_prompt(schema)

    # 🔁 Load prompt template from file
    with open("config/prompt_template.txt", "r") as f:
        template = f.read()

    # 🔀 Format the template with variables
    prompt = template.format(
        user_query=user_query,
        role=role,
        schema_text=schema_text
    )

    return prompt
