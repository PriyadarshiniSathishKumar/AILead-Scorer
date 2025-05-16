import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.lead_scoring import score_leads, validate_lead_data, preprocess_lead_data

def show_lead_upload_page():
    """Display the lead upload and scoring page"""
    st.title("Lead Upload & Scoring")
    st.markdown("Upload your leads and get AI-powered scoring to prioritize your efforts")
    
    # Create tabs for CSV upload and manual entry
    tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])
    
    with tab1:
        st.subheader("Upload Leads CSV")
        
        # Sample CSV template
        st.markdown("📝 **CSV format should include these columns:**")
        st.markdown("- Name - Lead's full name")
        st.markdown("- Contact - Phone number or email")
        st.markdown("- Location - City or region")
        st.markdown("- Product Interest - Product category they're interested in")
        st.markdown("- Last Contact Date - When you last connected (YYYY-MM-DD)")
        st.markdown("- Lead Source - How you acquired this lead")
        
        # Example CSV
        st.text("Example CSV format:")
        example_df = pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith'],
            'Contact': ['9876543210', 'jane@example.com'],
            'Location': ['Mumbai', 'Delhi'],
            'Product Interest': ['Insurance', 'Mutual Fund'],
            'Last Contact Date': ['2023-06-15', '2023-07-01'],
            'Lead Source': ['Website', 'Referral']
        })
        st.dataframe(example_df)
        
        # Sample CSV download 
        csv = example_df.to_csv(index=False)
        st.download_button(
            label="Download Sample CSV",
            data=csv,
            file_name="sample_leads.csv",
            mime="text/csv",
        )
        
        # Upload CSV
        uploaded_file = st.file_uploader("Upload your leads CSV", type=["csv"])
        
        if uploaded_file is not None:
            try:
                # Load the CSV file
                df = pd.read_csv(uploaded_file)
                
                # Validate the data
                is_valid, message = validate_lead_data(df)
                
                if is_valid:
                    # Preprocess data
                    df = preprocess_lead_data(df)
                    
                    # Score the leads
                    scored_df = score_leads(df)
                    
                    # Update session state
                    st.session_state.leads_df = scored_df
                    
                    # Success message
                    st.success(f"Successfully processed {len(scored_df)} leads!")
                    
                    # Show the scored leads
                    st.subheader("Scored Leads")
                    
                    # Define a function to color the rows based on score
                    def highlight_status(s):
                        if s['Status'] == 'Hot':
                            return ['background-color: #d4edda'] * len(s)
                        elif s['Status'] == 'Warm':
                            return ['background-color: #fff3cd'] * len(s)
                        else:  # Cold
                            return ['background-color: #f8d7da'] * len(s)
                    
                    # Apply styling and display
                    st.dataframe(scored_df.style.apply(highlight_status, axis=1))
                    
                    # Show counts by status
                    st.subheader("Lead Summary")
                    col1, col2, col3 = st.columns(3)
                    
                    hot_count = len(scored_df[scored_df['Status'] == 'Hot'])
                    warm_count = len(scored_df[scored_df['Status'] == 'Warm'])
                    cold_count = len(scored_df[scored_df['Status'] == 'Cold'])
                    
                    col1.metric("Hot Leads", hot_count)
                    col2.metric("Warm Leads", warm_count)
                    col3.metric("Cold Leads", cold_count)
                    
                    # Tips based on lead analysis
                    st.subheader("AI Recommendations")
                    
                    if hot_count > 0:
                        st.info(f"🔥 You have {hot_count} hot leads! Focus on closing these immediately with direct calls.")
                    
                    if warm_count > 0:
                        st.info(f"⚠️ Nurture your {warm_count} warm leads with regular follow-ups and address any objections they might have.")
                    
                    if cold_count > 0:
                        st.info(f"❄️ For your {cold_count} cold leads, try a new approach or consider reserving them for special promotions.")
                        
                else:
                    st.error(f"Error in data: {message}")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    with tab2:
        st.subheader("Manual Lead Entry")
        
        # Create form for manual entry
        with st.form("lead_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name")
                contact = st.text_input("Contact (Phone/Email)")
                location = st.text_input("Location")
            
            with col2:
                product_interest = st.selectbox(
                    "Product Interest",
                    [
                        "Life Insurance", 
                        "Health Insurance", 
                        "Motor Insurance",
                        "Investment", 
                        "Mutual Funds", 
                        "Fixed Deposit",
                        "Personal Loan",
                        "Home Loan",
                        "Credit Card",
                        "Other"
                    ]
                )
                
                last_contact = st.date_input("Last Contact Date", datetime.today())
                
                lead_source = st.selectbox(
                    "Lead Source",
                    [
                        "Referral", 
                        "Website", 
                        "Social Media",
                        "Cold Call", 
                        "Exhibition", 
                        "Advertisement",
                        "Existing Customer",
                        "Partner",
                        "Other"
                    ]
                )
            
            submitted = st.form_submit_button("Add Lead")
            
            if submitted:
                if name and contact:
                    # Create a new lead entry
                    new_lead = pd.DataFrame({
                        'Name': [name],
                        'Contact': [contact],
                        'Location': [location],
                        'Product Interest': [product_interest],
                        'Last Contact Date': [last_contact],
                        'Lead Source': [lead_source]
                    })
                    
                    # Score the lead
                    scored_lead = score_leads(new_lead)
                    
                    # Append to existing leads
                    if st.session_state.leads_df.empty:
                        st.session_state.leads_df = scored_lead
                    else:
                        st.session_state.leads_df = pd.concat([st.session_state.leads_df, scored_lead], ignore_index=True)
                    
                    # Success message
                    st.success(f"Added lead: {name} (Score: {scored_lead.iloc[0]['Score']}, Status: {scored_lead.iloc[0]['Status']})")
                else:
                    st.error("Name and Contact are required fields")
        
        # Show current leads if there are any
        if not st.session_state.leads_df.empty:
            st.subheader("Your Leads")
            
            # Define a function to color the rows based on score
            def highlight_status(s):
                if s['Status'] == 'Hot':
                    return ['background-color: #d4edda'] * len(s)
                elif s['Status'] == 'Warm':
                    return ['background-color: #fff3cd'] * len(s)
                else:  # Cold
                    return ['background-color: #f8d7da'] * len(s)
            
            # Apply styling and display
            st.dataframe(st.session_state.leads_df.style.apply(highlight_status, axis=1))
