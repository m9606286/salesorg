import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="業務組織圖", layout="wide")

# ------------------ Excel 路徑 ------------------
BASE_DIR = os.path.dirname(__file__)
EXCEL_FILE = os.path.join(BASE_DIR, "agents.xlsx")

if not os.path.exists(EXCEL_FILE):
    st.error(f"找不到 Excel 檔案: {EXCEL_FILE}\n請確認檔案已上傳到專案根目錄")
    st.stop()

# ------------------ 讀取 Excel ------------------
@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)

df = load_data()

# ------------------ 登入 ------------------
st.title("業務組織系統")
user_id = st.text_input("請輸入身分證字號登入:")

if user_id:
    user_row = df[df["身分證字號"] == user_id]
    if user_row.empty:
        st.error("身分證字號不存在！")
        st.stop()
    else:
        role = user_row.iloc[0]["角色"]
        user_name = user_row.iloc[0]["業務"]
        st.success(f"歡迎 {user_name} ({role}) 登入")

        # ------------------ 內勤 staff 可篩選營業處 ------------------
        if role == "staff":
            branch_options = df["營業處"].unique()
            branch_select = st.multiselect("篩選營業處", branch_options, default=branch_options)
            df_filtered = df[df["營業處"].isin(branch_select)]
        else:
            # agent 只能看到自己 + 下線
            def get_subordinates(df, user_id):
                subs = df[df["直屬身分證字號"] == user_id]["身分證字號"].tolist()
                all_ids = [user_id]
                for sub in subs:
                    all_ids += get_subordinates(df, sub)
                return all_ids
            visible_ids = get_subordinates(df, user_id)
            df_filtered = df[df["身分證字號"].isin(visible_ids)]

        # ------------------ 建立組織圖 ------------------
        G = nx.DiGraph()
        for _, row in df_filtered.iterrows():
            G.add_node(row["身分證字號"], label=row["業務"])
        for _, row in df_filtered.iterrows():
            if pd.notna(row["直屬身分證字號"]):
                G.add_edge(row["直屬身分證字號"], row["身分證字號"])

        # ------------------ 樹狀層級排列 ------------------
        def hierarchy_pos(G, root=None):
            if root is None:
                roots = [n for n,d in G.in_degree() if d==0]
                root = roots[0] if roots else list(G.nodes)[0]
            pos = {}
            def _hierarchy_pos(G, node, x=0, y=0, dx=1.0):
                children = list(G.successors(node))
                pos[node] = (x, y)
                if len(children) != 0:
                    width = dx / len(children)
                    nextx = x - dx/2 - width/2
                    for child in children:
                        nextx += width
                        _hierarchy_pos(G, child, nextx, y-1, width)
            _hierarchy_pos(G, root)
            return pos

        pos = hierarchy_pos(G)
        labels = nx.get_node_attributes(G, "label")
        plt.figure(figsize=(12,6))
        nx.draw(
            G, pos, with_labels=True, labels=labels,
            node_size=2000, node_color="skyblue", arrows=True,
            font_size=10
        )
        st.pyplot(plt)
