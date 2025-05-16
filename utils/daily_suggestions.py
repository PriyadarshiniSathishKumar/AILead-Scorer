import pandas as pd
import numpy as np
from datetime import datetime

def get_daily_suggestions():
    """
    Generate daily product suggestions based on day, trends, and rule-based logic
    
    Returns:
        list: List of dictionaries with product suggestions
    """
    today = datetime.now()
    day_of_week = today.weekday()  # 0-6 (Monday is 0)
    month = today.month
    
    # Base suggestions that work anytime
    base_suggestions = [
        {
            "product": "Term Life Insurance",
            "reason": "Always a high-commission product with essential protection for customers",
            "approach": "Focus on family security and peace of mind",
            "icon": "shield-check"
        },
        {
            "product": "Health Insurance",
            "reason": "Year-round necessity with increasing awareness",
            "approach": "Emphasize rising healthcare costs and tax benefits",
            "icon": "heart-pulse"
        },
        {
            "product": "SIP Investment Plans",
            "reason": "Long-term wealth building solution for all customer segments",
            "approach": "Start with small amounts and show compounding benefits",
            "icon": "trending-up"
        }
    ]
    
    # Day of week specific suggestions
    day_specific = {
        0: {  # Monday
            "product": "Accident Insurance",
            "reason": "Start of work week - people think about safety",
            "approach": "Quick 10-minute signup for year-long protection",
            "icon": "alert-triangle"
        },
        1: {  # Tuesday
            "product": "Child Education Plans",
            "reason": "Parents are in planning mode mid-week",
            "approach": "Show long-term education cost inflation data",
            "icon": "book-open"
        },
        2: {  # Wednesday
            "product": "Retirement Plans",
            "reason": "Mid-week is ideal for long-term planning discussions",
            "approach": "Use retirement calculators to show the gap",
            "icon": "umbrella"
        },
        3: {  # Thursday
            "product": "Health Insurance Add-ons",
            "reason": "Good day for upgrading existing customers",
            "approach": "Critical illness and outpatient coverage upsells",
            "icon": "plus-circle"
        },
        4: {  # Friday
            "product": "Travel Insurance",
            "reason": "Weekend trip planning makes this relevant",
            "approach": "Quick digital policy issuance for weekend travelers",
            "icon": "map"
        },
        5: {  # Saturday
            "product": "Family Floater Policies",
            "reason": "Weekend family time makes protection relevant",
            "approach": "Cover the whole family under one premium",
            "icon": "users"
        },
        6: {  # Sunday
            "product": "Investment Review",
            "reason": "Relaxed day for financial planning",
            "approach": "Offer free portfolio assessment and rebalancing",
            "icon": "bar-chart-2"
        }
    }
    
    # Seasonal suggestions
    seasonal_suggestions = []
    
    # March-end financial year closing
    if month == 3:
        seasonal_suggestions.append({
            "product": "Tax-saving ELSS Funds",
            "reason": "Financial year ending - tax saving rush",
            "approach": "Last chance for tax deductions this fiscal year",
            "icon": "file-minus"
        })
    
    # Festival season (October-November)
    if month in [10, 11]:
        seasonal_suggestions.append({
            "product": "Gold Investment Plans",
            "reason": "Festival season increases interest in gold",
            "approach": "Digital gold as a modern alternative to physical gold",
            "icon": "award"
        })
    
    # Monsoon season (June-September)
    if month in [6, 7, 8, 9]:
        seasonal_suggestions.append({
            "product": "Home Insurance",
            "reason": "Weather-related incidents increase during monsoon",
            "approach": "Protect against water damage and other monsoon risks",
            "icon": "home"
        })
    
    # Summer vacation season (April-May)
    if month in [4, 5]:
        seasonal_suggestions.append({
            "product": "International Travel Insurance",
            "reason": "Peak summer vacation planning season",
            "approach": "Comprehensive coverage for foreign trips",
            "icon": "globe"
        })
    
    # Combine suggestions
    all_suggestions = []
    
    # Add day-specific suggestion first
    all_suggestions.append(day_specific[day_of_week])
    
    # Add seasonal suggestions if available
    all_suggestions.extend(seasonal_suggestions)
    
    # Fill remaining spots with base suggestions
    remaining_slots = 5 - len(all_suggestions)
    all_suggestions.extend(base_suggestions[:remaining_slots])
    
    return all_suggestions[:5]  # Return at most 5 suggestions
