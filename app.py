import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json
import requests
import os
from datetime import datetime
from assets.lottie_animations import load_lottieurl, load_lottiefile
import pages.lead_upload as lead_upload
import pages.ai_coach as ai_coach
import pages.daily_suggestions as daily_suggestions
import pages.dashboard as dashboard

# Set page configuration
st.set_page_config(
    page_title="GroMo AI Sales Coach",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state variables
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = pd.DataFrame(columns=[
        'Name', 'Contact', 'Location', 'Product Interest', 
        'Last Contact Date', 'Lead Source', 'Score', 'Status'
    ])

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'total_interactions' not in st.session_state:
    st.session_state.total_interactions = 0

if 'suggestion_clicks' not in st.session_state:
    st.session_state.suggestion_clicks = 0

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        font-weight: normal;
        margin-bottom: 2rem;
        color: #666;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        background: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .hot-lead {
        background-color: #d4edda;
    }
    .warm-lead {
        background-color: #fff3cd;
    }
    .cold-lead {
        background-color: #f8d7da;
    }
    .stButton button {
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("GroMo AI Sales Coach")

# Load and display sidebar logo/animation
sales_lottie = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_xbf1be8x.json')
st_lottie(sales_lottie, speed=1, height=200, key="sidebar_animation")

# Navigation
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Lead Upload & Scoring", "AI Sales Coach", "Daily Sales Suggestions", "Performance Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Today's Stats")
st.sidebar.metric("Leads Uploaded", len(st.session_state.leads_df))
st.sidebar.metric("Hot Leads", 
                 len(st.session_state.leads_df[st.session_state.leads_df['Status'] == 'Hot']) if 'Status' in st.session_state.leads_df.columns else 0)
st.sidebar.metric("Coach Interactions", st.session_state.total_interactions)

# Main content area
if page == "Home":
    # Header with animation
    st.markdown('<div class="main-header">Welcome to GroMo AI Sales Coach</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Boost your sales with AI-powered lead scoring & coaching</div>', 
                unsafe_allow_html=True)
    
    # Main dashboard animation
    dashboard_lottie = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_w4f2qg8o.json')
    st_lottie(dashboard_lottie, speed=1, height=300, key="dashboard_animation")
    
    # Quick stats in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Total Leads", len(st.session_state.leads_df))
        st.markdown("Upload and score your leads to improve conversion")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("AI Coach Interactions", st.session_state.total_interactions)
        st.markdown("Get personalized sales advice from our AI Coach")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Daily Suggestions", st.session_state.suggestion_clicks)
        st.markdown("Explore product recommendations based on trends")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Motivational quote
    st.markdown("---")
    st.markdown("### 💡 Daily Insight")
    quotes = [
        "\"The successful warrior is the average man, with laser-like focus.\" - Bruce Lee",
        "\"Don't watch the clock; do what it does. Keep going.\" - Sam Levenson",
        "\"Success is not final, failure is not fatal: It is the courage to continue that counts.\" - Winston Churchill",
        "\"Quality performance starts with a positive attitude.\" - Jeffrey Gitomer",
        "\"Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.\" - Thomas Edison"
    ]
    import random
    st.info(random.choice(quotes))
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Upload Leads", use_container_width=True):
            page = "Lead Upload & Scoring"
            st.rerun()
    with col2:
        if st.button("Chat with AI Coach", use_container_width=True):
            page = "AI Sales Coach"
            st.rerun()
    with col3:
        if st.button("View Today's Suggestions", use_container_width=True):
            page = "Daily Sales Suggestions"
            st.rerun()

elif page == "Lead Upload & Scoring":
    lead_upload.show_lead_upload_page()
    
elif page == "AI Sales Coach":
    ai_coach.show_ai_coach_page()
    
elif page == "Daily Sales Suggestions":
    daily_suggestions.show_daily_suggestions_page()
    
elif page == "Performance Dashboard":
    dashboard.show_dashboard_page()
