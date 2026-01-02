import streamlit as st
import pandas as pd
import os

st.title("測試 Excel 是否能讀取")

BASE_DIR = os.path.dirname(__file__)
EXCEL_FILE = os.path.join(BASE_DIR, "agents.xlsx")

if not os.path.exists(EXCEL_FILE):
    st.error(f"找不到 Excel 檔案: {EXCEL_FILE}")
    st.stop()

df = pd.read_excel(EXCEL_FILE)
st.write(df)
