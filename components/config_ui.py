import streamlit as st
import json
import os

def render_config_screen():
    st.markdown("## ⚙️ RAG-Based Chatbot Configuration")

    # Prompt Template
    with st.expander("Prompt Configuration"):
        prompt_template_path = "config/prompt_template.txt"
        if os.path.exists(prompt_template_path):
            prompt_text = open(prompt_template_path).read()
        else:
            prompt_text = ""

        updated_prompt = st.text_area("User Prompt Template", value=prompt_text, height=200)
        if st.button("💾 Save Prompt"):
            with open(prompt_template_path, "w") as f:
                f.write(updated_prompt)
            st.success("Prompt saved.")

    # Top K
    top_k = st.slider("Top K Documents to Retrieve", min_value=1, max_value=20, value=5)
    # 🔽 Model Configuration
    st.markdown("### 🧠 Generation Model Settings")
    model_config_path = "config/model_config.json"
    default_model = "Gemini-Pro"
    available_models = ["Gemini-Pro", "GPT-4", "SQLCoder", "LLaMA-3-8B", "T5-NL2SQL"]

    # Load current config
    if os.path.exists(model_config_path):
        with open(model_config_path) as f:
            model_config = json.load(f)
            default_model = model_config.get("generation_model", default_model)

    selected_model = st.selectbox("Select Generation Model", available_models, index=available_models.index(default_model))

    if st.button("💾 Save Model Configuration"):
        with open(model_config_path, "w") as f:
            json.dump({"generation_model": selected_model}, f)
        st.success(f"Saved model: {selected_model}")

    # 🛡️ Roles
    # st.markdown("### 🔐 Role & Access Configuration")
    # with open("config/roles.json") as f:
    #     roles = json.load(f)
    #     st.json(roles)

    # # 🗄️ Schema
    # st.markdown("### 🏗️ Schema Configuration")
    # with open("config/schema.json") as f:
    #     schema = json.load(f)
    #     st.json(schema)
