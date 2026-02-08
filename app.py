import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

st.set_page_config(page_title="LLM Code Generator", layout="centered")
st.title("💻 LLM Code Generator")
st.write("Generate code using Groq LLaMA-3.1 (free tier)")

prompt = st.text_area(
    "Describe the code you want",
    placeholder="Example: Write Python code for binary search"
)

language = st.selectbox(
    "Select programming language",
    ["Python", "Java", "C", "JavaScript"]
)

if st.button("Generate Code"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt")
    else:
        try:
            with st.spinner("Generating code..."):
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        # ✅ CURRENT SUPPORTED MODEL
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Write {language} code for: {prompt}"
                            }
                        ],
                        "temperature": 0.2
                    },
                    timeout=30
                )

                data = response.json()

                if "choices" in data and len(data["choices"]) > 0:
                    code = data["choices"][0]["message"]["content"]
                    st.success("✅ Code generated successfully")
                    st.code(code, language=language.lower())
                else:
                    st.error("❌ Unexpected API response")
                    st.write(data)

        except Exception as e:
            st.error(f"❌ Error: {e}")
