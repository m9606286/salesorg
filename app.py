import streamlit as st
import pandas as pd
import os

df = pd.read_excel("agents.xlsx")

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "營業處": "branch",
    "業務": "name",
    "職階": "level",
    "直屬主管": "manager",
    "身分證字號": "id",
    "直屬身分證字號": "manager_id",
    "角色": "role"
})

st.subheader("營業處人員名單")

branches = sorted(df["branch"].dropna().unique())
selected_branch = st.selectbox("選擇營業處", branches)

branch_df = df[df["branch"] == selected_branch]

st.dataframe(
    branch_df[["name", "level", "manager", "role"]],
    use_container_width=True
)



