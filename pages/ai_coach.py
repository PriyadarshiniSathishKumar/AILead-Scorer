import streamlit as st
from streamlit_lottie import st_lottie
import time
from utils.ai_coach import generate_ai_response, get_sales_tip_of_the_day
from assets.lottie_animations import load_lottieurl, load_lottiefile

def show_ai_coach_page():
    """Display the AI sales coach chat page"""
    st.title("AI Sales Coach")
    st.markdown("Get personalized sales advice and coaching")
    
    # Display tips of the day
    st.info(f"💡 **Tip of the day:** {get_sales_tip_of_the_day()}")
    
    # Two-column layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Chat container with styling
        st.markdown("""
        <style>
        .chat-container {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
        }
        .user-message {
            background-color: #e1f5fe;
            border-radius: 18px 18px 0 18px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
            margin-left: auto;
            margin-right: 10px;
        }
        .bot-message {
            background-color: #f0f0f0;
            border-radius: 18px 18px 18px 0;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
            margin-right: auto;
            margin-left: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Initialize chat history if not exists
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
            # Add a welcome message if chat is empty
            welcome_message = {
                "role": "assistant", 
                "content": "Hi there! I'm your AI Sales Coach. Ask me any questions about sales techniques, handling objections, or product pitches. What would you like help with today?"
            }
            st.session_state.chat_history.append(welcome_message)
        
        # Display chat messages
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Ask me anything about sales:", key="user_query")
            submitted = st.form_submit_button("Send")
            
            if submitted and user_input:
                # Add user message to chat
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Update chat history display
                st.rerun()
                
    # Handle AI response (outside the form to avoid rerun issues)
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        user_query = st.session_state.chat_history[-1]["content"]
        
        # Show a typing indicator
        with col1:
            typing_placeholder = st.empty()
            typing_placeholder.markdown("*AI Coach is typing...*")
            
            # Generate AI response
            ai_response = generate_ai_response(user_query, st.session_state.chat_history)
            
            # Simulate typing delay for better user experience
            time.sleep(1)
            typing_placeholder.empty()
            
            # Add AI response to chat
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Increment interaction counter
            st.session_state.total_interactions += 1
            
            # Update display
            st.rerun()
    
    with col2:
        # Display a coaching animation
        coach_lottie = load_lottieurl('https://assets4.lottiefiles.com/private_files/lf30_dln2gqhg.json')
        st_lottie(coach_lottie, key="coach_animation", height=300)
        
        # Common sales questions
        st.subheader("Common Sales Questions")
        
        common_questions = [
            "How do I close a hesitant lead?",
            "What's the best way to handle price objections?",
            "How to create an effective sales pitch?",
            "Tips for cross-selling insurance products?",
            "How to build rapport quickly?",
            "Best follow-up strategies for cold leads?"
        ]
        
        for question in common_questions:
            if st.button(question, key=f"q_{question[:10]}"):
                # Add question to chat
                st.session_state.chat_history.append({"role": "user", "content": question})
                # Rerun to trigger the AI response
                st.rerun()
