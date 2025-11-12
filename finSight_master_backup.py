import os
START_STREAMLIT = os.getenv("START_STREAMLIT","true").lower() == "true"
if not START_STREAMLIT:
    print("[INFO] Streamlit auto-start is uitgeschakeld. Je kunt coderen zonder dat de terminal wordt geblokkeerd.")
    exit()
import os
START_STREAMLIT = os.getenv("START_STREAMLIT","true").lower() == "true"
if not START_STREAMLIT:
    print("[INFO] Streamlit auto-start is uitgeschakeld. Je kunt coderen zonder dat de terminal wordt geblokkeerd.")
    exit()
import streamlit as st
import os
from utils import validate_keys

# Wachtwoord bescherming
password = os.getenv("FIN_SIGHT_PASS", "changeme")
def check_password():
    st.session_state["authenticated"] = False if "authenticated" not in st.session_state else st.session_state["authenticated"]
    if not st.session_state["authenticated"]:
        input_pass = st.text_input("Voer wachtwoord in:", type="password")
        if input_pass == password:
            st.session_state["authenticated"] = True
        else:
            st.warning("Onjuist wachtwoord")
            st.stop()

check_password()

st.title("FinSight Global AI Dashboard")
st.write("Welkom bij je AI trading dashboard. PAPER MODE is standaard actief.")

paper_mode = validate_keys()
st.write(f"Paper mode: {paper_mode}")
