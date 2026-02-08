import streamlit as st
import sqlite3
import pandas as pd
from matcher import find_best_match

st.set_page_config(page_title="SkillSwap AI", page_icon="🤝", layout="wide")

# Database Setup
def init_db():
    conn = sqlite3.connect('skills.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (name TEXT, teaches TEXT, needs TEXT)''')
    conn.commit()
    conn.close()

def add_user(name, teaches, needs):
    conn = sqlite3.connect('skills.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, teaches, needs) VALUES (?, ?, ?)", (name, teaches, needs))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('skills.db')
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

init_db()

st.title("🤝 SkillSwap AI: Live Community")

with st.sidebar:
    st.header("📝 Register New Member")
    new_name = st.text_input("Name")
    new_teach = st.text_input("I can teach...")
    new_learn = st.text_input("I want to learn...")
    
    if st.button("Save to Database"):
        if new_name and new_teach:
            add_user(new_name, new_teach, new_learn)
            st.success(f"Added {new_name}!")
        else:
            st.error("Name and Skills are required.")

# Main Application Logic
df = get_all_users()

tab1, tab2 = st.tabs(["🔍 Find a Match", "📋 Member Directory"])

with tab1:
    search_query = st.text_input("What do you want to learn today?")
    if st.button("Search AI Database"):
        if not df.empty and search_query:
            match_idx = find_best_match(search_query, df["teaches"].tolist())
            match = df.iloc[match_idx]
            st.balloons()
            st.info(f"**Best Match Found:** {match['name']} can teach you **{match['teaches']}**!")
        elif df.empty:
            st.warning("Database is empty. Please register members in the sidebar first.")

with tab2:
    st.subheader("Current Community Members")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No members registered yet.")
