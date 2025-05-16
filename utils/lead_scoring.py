import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def score_leads(df):
    """
    Score leads based on various factors like recency, product interest, location
    
    Args:
        df (pd.DataFrame): DataFrame containing lead information
    
    Returns:
        pd.DataFrame: DataFrame with added Score and Status columns
    """
    
    if df.empty:
        return df
    
    # Create a copy to avoid SettingWithCopyWarning
    scored_df = df.copy()
    
    # Initialize score column
    scored_df['Score'] = 50  # Start with neutral score
    
    # Score based on Last Contact Date (recency)
    # More recent contacts get higher scores
    if 'Last Contact Date' in scored_df.columns:
        try:
            scored_df['Last Contact Date'] = pd.to_datetime(scored_df['Last Contact Date'])
            today = pd.to_datetime(datetime.today())
            
            # Calculate days since last contact
            scored_df['Days Since Contact'] = (today - scored_df['Last Contact Date']).dt.days
            
            # Score based on recency (higher for more recent contacts)
            scored_df.loc[scored_df['Days Since Contact'] <= 7, 'Score'] += 20  # Very recent (within week)
            scored_df.loc[(scored_df['Days Since Contact'] > 7) & (scored_df['Days Since Contact'] <= 30), 'Score'] += 10  # Recent (within month)
            scored_df.loc[scored_df['Days Since Contact'] > 90, 'Score'] -= 15  # Very old contact
            
            # Drop the temporary column
            scored_df = scored_df.drop('Days Since Contact', axis=1)
        except Exception as e:
            print(f"Error processing Last Contact Date: {e}")
    
    # Score based on Product Interest
    if 'Product Interest' in scored_df.columns:
        # Example: Higher score for premium products
        premium_products = ['insurance', 'mutual fund', 'premium', 'gold', 'investment']
        scored_df['Product Interest'] = scored_df['Product Interest'].astype(str).str.lower()
        
        for product in premium_products:
            scored_df.loc[scored_df['Product Interest'].str.contains(product), 'Score'] += 10
    
    # Score based on Lead Source
    if 'Lead Source' in scored_df.columns:
        # Example: Higher score for referrals which typically convert better
        high_quality_sources = ['referral', 'existing customer', 'partner', 'website']
        scored_df['Lead Source'] = scored_df['Lead Source'].astype(str).str.lower()
        
        for source in high_quality_sources:
            scored_df.loc[scored_df['Lead Source'].str.contains(source), 'Score'] += 15
            
        # Lower score for cold sources
        cold_sources = ['cold call', 'exhibition', 'advertisement']
        for source in cold_sources:
            scored_df.loc[scored_df['Lead Source'].str.contains(source), 'Score'] -= 5
    
    # Ensure scores are within 0-100 range
    scored_df['Score'] = scored_df['Score'].clip(0, 100)
    
    # Categorize the leads based on scores
    scored_df['Status'] = 'Cold'
    scored_df.loc[scored_df['Score'] >= 50, 'Status'] = 'Warm'
    scored_df.loc[scored_df['Score'] >= 80, 'Status'] = 'Hot'
    
    return scored_df

def validate_lead_data(df):
    """
    Validate the lead data for required fields and format
    
    Args:
        df (pd.DataFrame): DataFrame containing lead information
    
    Returns:
        tuple: (is_valid, message)
    """
    # Check for required columns
    required_columns = ['Name', 'Contact']
    for col in required_columns:
        if col not in df.columns:
            return False, f"Missing required column: {col}"
    
    # Check for empty DataFrame
    if df.empty:
        return False, "The uploaded file contains no data"
    
    # Validate phone numbers if present
    if 'Contact' in df.columns:
        # Basic phone validation - at least 10 digits
        invalid_phones = df[~df['Contact'].astype(str).str.contains(r'\d{10}')]
        if not invalid_phones.empty:
            return False, f"Invalid phone number format for {len(invalid_phones)} leads. Please ensure all numbers have at least 10 digits."
    
    return True, "Data validated successfully"

def preprocess_lead_data(df):
    """
    Preprocess the lead data - handle missing values, format dates, etc.
    
    Args:
        df (pd.DataFrame): DataFrame containing lead information
    
    Returns:
        pd.DataFrame: Preprocessed DataFrame
    """
    # Create a copy to avoid SettingWithCopyWarning
    cleaned_df = df.copy()
    
    # Handle missing values
    if 'Last Contact Date' in cleaned_df.columns:
        # Fill missing dates with today's date
        cleaned_df['Last Contact Date'] = pd.to_datetime(
            cleaned_df['Last Contact Date'], 
            errors='coerce'
        )
        cleaned_df['Last Contact Date'].fillna(pd.Timestamp.today(), inplace=True)
    
    if 'Product Interest' in cleaned_df.columns:
        cleaned_df['Product Interest'].fillna('Unknown', inplace=True)
        
    if 'Lead Source' in cleaned_df.columns:
        cleaned_df['Lead Source'].fillna('Other', inplace=True)
        
    if 'Location' in cleaned_df.columns:
        cleaned_df['Location'].fillna('Unknown', inplace=True)
    
    return cleaned_df
