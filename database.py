import streamlit as st
import pandas as pd
from supabase import create_client

def get_db_connection():
    """Establishes connection to Supabase using secrets."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_data(ttl=600)
def fetch_student_data():
    """Fetches all student records for the Teacher Dashboard."""
    supabase = get_db_connection()
    response = supabase.table("students").select("*").execute()
    return pd.DataFrame(response.data)

def fetch_single_student(student_name):
    """Fetches a specific student's record with the correct .select() chain."""
    supabase = get_db_connection()
    # Fixed the .select().eq() chain and ensured 4-space indentation
    response = supabase.table("students").select("*").eq("name", student_name).execute()
    return pd.DataFrame(response.data)

@st.cache_data(ttl=3600)
def fetch_materials():
    """Fetches all learning modules from the materials table."""
    supabase = get_db_connection()
    response = supabase.table("materials").select("*").execute()
    return pd.DataFrame(response.data)