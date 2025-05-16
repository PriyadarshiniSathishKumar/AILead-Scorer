import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_lottie import st_lottie
from assets.lottie_animations import load_lottieurl, load_lottiefile

def show_dashboard_page():
    """Display the performance dashboard page"""
    st.title("Performance Dashboard")
    st.markdown("Track your sales performance metrics and lead statistics")
    
    # Dashboard animation
    dashboard_lottie = load_lottieurl('https://assets9.lottiefiles.com/packages/lf20_tllkbdio.json')
    st_lottie(dashboard_lottie, speed=1, height=200, key="dashboard_animation")
    
    # Key metrics in expandable card
    with st.expander("📊 Key Metrics", expanded=True):
        # Row of metrics 
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Total leads
            st.metric(
                "Total Leads", 
                len(st.session_state.leads_df),
                delta=None
            )
            
        with col2:
            # Hot leads percentage
            hot_leads = len(st.session_state.leads_df[st.session_state.leads_df['Status'] == 'Hot']) if not st.session_state.leads_df.empty and 'Status' in st.session_state.leads_df.columns else 0
            hot_percentage = round((hot_leads / len(st.session_state.leads_df) * 100) if len(st.session_state.leads_df) > 0 else 0, 1)
            
            st.metric(
                "Hot Leads %",
                f"{hot_percentage}%",
                delta=None
            )
            
        with col3:
            # AI Coach interactions
            st.metric(
                "Coach Interactions",
                st.session_state.total_interactions,
                delta=None
            )
            
        with col4:
            # Suggestion clicks
            st.metric(
                "Suggestions Utilized",
                st.session_state.suggestion_clicks,
                delta=None
            )
    
    # Lead distribution chart
    with st.expander("🔥 Lead Status Distribution", expanded=True):
        if not st.session_state.leads_df.empty and 'Status' in st.session_state.leads_df.columns:
            # Count leads by status
            status_counts = st.session_state.leads_df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            # Create color map
            color_map = {'Hot': '#4CAF50', 'Warm': '#FFC107', 'Cold': '#f44336'}
            
            # Create pie chart
            fig = px.pie(
                status_counts, 
                values='Count', 
                names='Status',
                title='Lead Distribution by Status',
                color='Status',
                color_discrete_map=color_map,
                hole=0.4
            )
            
            # Update layout
            fig.update_layout(
                legend_title_text='Lead Status',
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Upload leads to see distribution chart")
    
    # Lead sources analysis
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📋 Lead Sources", expanded=True):
            if not st.session_state.leads_df.empty and 'Lead Source' in st.session_state.leads_df.columns:
                # Count leads by source
                source_counts = st.session_state.leads_df['Lead Source'].value_counts().reset_index()
                source_counts.columns = ['Lead Source', 'Count']
                
                # Create bar chart
                fig = px.bar(
                    source_counts, 
                    x='Lead Source', 
                    y='Count',
                    title='Lead Count by Source',
                    color='Count',
                    color_continuous_scale=['#2196F3', '#4CAF50']
                )
                
                # Update layout
                fig.update_layout(
                    xaxis_title='Lead Source',
                    yaxis_title='Number of Leads',
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Upload leads to see sources analysis")
    
    with col2:
        with st.expander("🔍 Product Interest", expanded=True):
            if not st.session_state.leads_df.empty and 'Product Interest' in st.session_state.leads_df.columns:
                # Count leads by product interest
                product_counts = st.session_state.leads_df['Product Interest'].value_counts().reset_index()
                product_counts.columns = ['Product Interest', 'Count']
                
                # Create horizontal bar chart
                fig = px.bar(
                    product_counts, 
                    y='Product Interest', 
                    x='Count',
                    title='Interest by Product',
                    orientation='h',
                    color='Count',
                    color_continuous_scale=['#2196F3', '#4CAF50']
                )
                
                # Update layout
                fig.update_layout(
                    yaxis_title='Product',
                    xaxis_title='Number of Leads',
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Upload leads to see product interest analysis")
    
    # Lead scoring distribution
    with st.expander("📈 Lead Score Distribution", expanded=True):
        if not st.session_state.leads_df.empty and 'Score' in st.session_state.leads_df.columns:
            # Create histogram
            fig = px.histogram(
                st.session_state.leads_df, 
                x='Score',
                nbins=20,
                title='Distribution of Lead Scores',
                color_discrete_sequence=['#2196F3']
            )
            
            # Add vertical lines for score categories
            fig.add_vline(x=50, line_dash="dash", line_color="#FFC107", annotation_text="Warm Threshold")
            fig.add_vline(x=80, line_dash="dash", line_color="#4CAF50", annotation_text="Hot Threshold")
            
            # Update layout
            fig.update_layout(
                xaxis_title='Lead Score',
                yaxis_title='Number of Leads',
                bargap=0.1
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Upload leads to see score distribution")
    
    # Location analysis
    with st.expander("🌎 Geographic Distribution", expanded=True):
        if not st.session_state.leads_df.empty and 'Location' in st.session_state.leads_df.columns:
            # Count leads by location
            location_counts = st.session_state.leads_df['Location'].value_counts().reset_index()
            location_counts.columns = ['Location', 'Count']
            
            # Sort by count
            location_counts = location_counts.sort_values('Count', ascending=False)
            
            # Create bar chart
            fig = px.bar(
                location_counts.head(10), 
                x='Location', 
                y='Count',
                title='Top 10 Locations by Lead Count',
                color='Count',
                color_continuous_scale=['#2196F3', '#4CAF50']
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title='Location',
                yaxis_title='Number of Leads',
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Upload leads to see geographic distribution")
    
    # Motivational section
    st.markdown("---")
    st.subheader("💪 Motivation Corner")
    
    # Get the current date for consistent daily quotes
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Quotes
    quotes = [
        {"text": "Success is not final, failure is not fatal: It is the courage to continue that counts.", "author": "Winston Churchill"},
        {"text": "The successful warrior is the average man, with laser-like focus.", "author": "Bruce Lee"},
        {"text": "Success seems to be connected with action. Successful people keep moving.", "author": "Conrad Hilton"},
        {"text": "The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack in will.", "author": "Vince Lombardi"},
        {"text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
        {"text": "The secret of success is to do the common thing uncommonly well.", "author": "John D. Rockefeller Jr."},
        {"text": "I find that the harder I work, the more luck I seem to have.", "author": "Thomas Jefferson"},
        {"text": "Success is walking from failure to failure with no loss of enthusiasm.", "author": "Winston Churchill"}
    ]
    
    # Use the date string to select a consistent quote for the day
    quote_index = sum(ord(c) for c in today) % len(quotes)
    quote = quotes[quote_index]
    
    # Display the quote
    st.info(f"\"{quote['text']}\" — {quote['author']}")
