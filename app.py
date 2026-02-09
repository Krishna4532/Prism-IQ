import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from src.database import fetch_student_data, fetch_single_student, fetch_materials
from src.ai_engine import get_ai_strategy

# --- 1. GLOBAL CONFIG ---
st.set_page_config(page_title="Prism IQ | Behavioral Analytics", page_icon="📐", layout="wide")

# Session State for Login Routing
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# --- 2. LOGIN GATEWAY ---
def show_login():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📐 PRISM IQ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>AI-Powered Behavioral Intelligence</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 🍎 Teacher Portal")
        st.write("Access full class metrics, 3D behavioral clusters, and Gemini AI interventions.")
        if st.button("Login as Educator", use_container_width=True, type="primary"):
            st.session_state.role = "teacher"
            st.rerun()
            
    with col2:
        st.success("### 🎓 Student Portal")
        st.write("Track your progress and access assigned learning materials.")
        # For demo, we'll assume the student is 'Krishna (Lead)'
        if st.button("Login as Student", use_container_width=True):
            st.session_state.role = "student"
            st.session_state.user_name = "Krishna (Lead)"
            st.rerun()

# --- 3. TEACHER DASHBOARD ---
def teacher_portal():
    st.sidebar.title("Admin Panel")
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.rerun()
    
    st.title("📊 Educator Insights")
    
    try:
        df = fetch_student_data()
        if not df.empty:
            # Clustering Math (K-Means)
            kmeans = KMeans(n_clusters=min(len(df), 4), random_state=42, n_init=10)
            df['cluster'] = kmeans.fit_predict(df[['time_spent', 'accuracy', 'hints_used']])
            persona_map = {0: "Strategic", 1: "At-Risk", 2: "Persistent", 3: "Frustrated"}
            df['persona'] = df['cluster'].map(persona_map)

            col_main, col_side = st.columns([2, 1])

            with col_main:
                st.subheader("🌐 Behavioral Spectrum (3D)")
                fig = px.scatter_3d(df, x='time_spent', y='accuracy', z='hints_used', 
                                    color='persona', hover_name='name', template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

            with col_side:
                st.subheader("🤖 AI Advice")
                target = st.selectbox("Select Student", df['name'])
                row = df[df['name'] == target].iloc[0]
                if st.button(f"Generate Strategy"):
                    with st.spinner("Gemini is analyzing..."):
                        advice = get_ai_strategy(target, row['persona'], row['accuracy'], row['hints_used'])
                        st.markdown(advice)
    except Exception as e:
        st.error(f"Error: {e}")

# --- 4. STUDENT PORTAL ---
def student_portal():
    st.sidebar.title("Student Hub")
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.rerun()

    name = st.session_state.user_name
    st.title(f"👋 Welcome back, {name}!")
    
    # Personal Stats
    student_df = fetch_single_student(name)
    if not student_df.empty:
        data = student_df.iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Accuracy", f"{data['accuracy']}%")
        c2.metric("Study Time", f"{data['time_spent']}m")
        c3.metric("Hints Used", data['hints_used'])
        st.progress(data['accuracy'] / 100)
    
    st.divider()
    
    # Materials
    st.subheader("📚 Assigned Materials")
    mat_df = fetch_materials()
    if not mat_df.empty:
        for _, m in mat_df.iterrows():
            with st.expander(f"{m['title']} ({m['category']})"):
                st.link_button("View Content", m['link'])
    else:
        st.info("No materials assigned yet.")

# --- 5. APP ROUTER ---
if st.session_state.role == "teacher":
    teacher_portal()
elif st.session_state.role == "student":
    student_portal()
else:
    show_login()