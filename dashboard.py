import streamlit as st
import json
st.title("QA Dashboard")
if st.button("Run Pipeline"):
    import subprocess
    subprocess.run(["python", "main.py"])
if st.checkbox("Show last report"):
    try:
        with open("reports/result.json") as f:
            data = json.load(f)
        st.json(data)
    except:
        st.warning("No report yet")