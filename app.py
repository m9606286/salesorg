import streamlit as st
import pandas as pd
import os

st.title("測試 Excel 讀取")

EXCEL_FILE = os.path.join(os.path.dirname(__file__), "agents.xlsx")

if not os.path.exists(EXCEL_FILE):
    st.error(f"找不到 Excel 檔案: {EXCEL_FILE}")
    st.stop()

df = pd.read_excel(EXCEL_FILE)
st.write(df)
