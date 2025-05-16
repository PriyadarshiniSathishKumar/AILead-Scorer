import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_lottie import st_lottie
from utils.daily_suggestions import get_daily_suggestions
from assets.lottie_animations import load_lottieurl, load_lottiefile

def show_daily_suggestions_page():
    """Display the daily sales suggestions page"""
    st.title("Daily Sales Suggestions")
    st.markdown(f"Personalized product recommendations for {datetime.now().strftime('%A, %B %d, %Y')}")
    
    # Get suggestions
    suggestions = get_daily_suggestions()
    
    # Animation at the top
    suggestion_lottie = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_uzvwjpkq.json')
    st_lottie(suggestion_lottie, speed=1, height=200, key="suggestion_animation")
    
    # Introduction text
    st.markdown("""
    Below are today's recommended products to focus on, based on current trends, 
    day of the week, and seasonal factors. Click on any card for more details.
    """)
    
    # Custom CSS for cards
    st.markdown("""
    <style>
    .suggestion-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .suggestion-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .product-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2196F3;
        margin-bottom: 10px;
    }
    .reason-text {
        color: #666;
        margin-bottom: 15px;
    }
    .approach-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
    }
    .approach-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display suggestions in two columns
    col1, col2 = st.columns(2)
    
    # Function to increment suggestion clicks
    def increment_suggestion_clicks():
        st.session_state.suggestion_clicks += 1
    
    # Display suggestions in cards
    for i, suggestion in enumerate(suggestions):
        # Alternate between columns
        with col1 if i % 2 == 0 else col2:
            # Create an expander for each suggestion
            with st.expander(f"**{suggestion['product']}**", expanded=True):
                st.markdown(f"<div class='suggestion-card'>", unsafe_allow_html=True)
                
                # Product title with icon
                st.markdown(f"<div class='product-title'>📊 {suggestion['product']}</div>", unsafe_allow_html=True)
                
                # Reason
                st.markdown(f"<div class='reason-text'><strong>Why today:</strong> {suggestion['reason']}</div>", unsafe_allow_html=True)
                
                # Approach section
                st.markdown(f"<div class='approach-section'>", unsafe_allow_html=True)
                st.markdown(f"<div class='approach-title'>Recommended Approach:</div>", unsafe_allow_html=True)
                st.markdown(f"{suggestion['approach']}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Action button
                if st.button(f"Use This Suggestion", key=f"suggestion_{i}", on_click=increment_suggestion_clicks):
                    st.success(f"Added '{suggestion['product']}' to your focus list for today!")
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional resources section
    st.markdown("---")
    st.subheader("Resources & Materials")
    
    tab1, tab2, tab3 = st.tabs(["Scripts & Templates", "Objection Handling", "Product Knowledge"])
    
    with tab1:
        st.markdown("""
        ### Sample Scripts
        
        **Opening line for cold calls:**
        > "Hello [Name], this is [Your Name] from GroMo. Many people in [Location] are using our [Product] to [Benefit]. I'm wondering if you've considered how this could help you too?"
        
        **Follow-up message:**
        > "Hi [Name], following up on our conversation about [Product]. I remembered you mentioned [Specific Need], and I thought of a solution that might work perfectly for you. Do you have 5 minutes to discuss this?"
        
        **Closing script:**
        > "Based on what you've shared, I believe [Product] would be an excellent fit because [Personalized Reason]. Would you like to proceed with setting it up today?"
        """)
        
    with tab2:
        st.markdown("""
        ### Common Objections & Responses
        
        **"It's too expensive"**
        > "I understand budget concerns are important. Let's look at the value over time. For just [break down cost], you get [list benefits]. Many clients find that the protection/returns outweigh the initial investment."
        
        **"I need to think about it"**
        > "That makes sense. To help you make the best decision, what specific aspects do you need to consider? This will help me provide you with exactly the information you need."
        
        **"I already have something similar"**
        > "That's great! May I ask what you currently have? There might be gaps in coverage/benefits that our solution addresses, or we might offer better terms on similar features."
        """)
        
    with tab3:
        st.markdown("""
        ### Key Product Highlights
        
        **Term Life Insurance**
        - Highest coverage for lowest premium
        - Tax benefits under Section 80C
        - Optional riders for critical illness, accidental death
        
        **Health Insurance**
        - Cashless treatment at 5000+ network hospitals
        - No claim bonus increasing coverage by 50% over 5 years
        - Free annual health check-ups
        
        **SIP Investments**
        - Start with as little as ₹500 per month
        - Automatic investment discipline
        - Rupee cost averaging benefits in volatile markets
        """)
