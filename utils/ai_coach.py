import requests
import json
import random
from datetime import datetime

def generate_ai_response(user_input, chat_history=None):
    """
    Generate AI coach response based on user input
    
    Args:
        user_input (str): User's question or prompt
        chat_history (list, optional): List of previous chat exchanges
        
    Returns:
        str: AI response
    """
    # If we're in a production environment, we would connect to a real AI model
    # For now, we'll use a simple rule-based approach with predefined responses
    
    # Convert to lowercase for matching
    input_lower = user_input.lower()
    
    # Define some categories and response templates
    responses = {
        "greeting": [
            "Hello! I'm your AI Sales Coach. How can I help you today?",
            "Hi there! Ready to boost your sales performance? What would you like to know?",
            "Greetings! I'm here to help you become a better salesperson. What's on your mind?"
        ],
        "closing": [
            "To close a lead effectively, focus on these key steps:\n\n1. Summarize the benefits specific to their needs\n2. Address any remaining objections directly\n3. Propose a clear next action\n4. Ask for the commitment confidently\n5. Maintain silence after asking for the sale",
            "The best closing technique is the one that feels natural to the conversation. Try the 'summary close' - recap all the benefits they've agreed with, then ask 'Does this solution work for you?'",
            "Closing is about timing. Look for buying signals like detailed questions, discussing implementation, or positive body language. Then ask a direct closing question like 'Are you ready to move forward?'"
        ],
        "objection": [
            "When handling objections, remember to:\n\n1. Listen completely without interrupting\n2. Acknowledge their concern as valid\n3. Ask clarifying questions to understand the real issue\n4. Respond to the actual concern, not just the surface objection\n5. Confirm you've addressed their concern before moving on",
            "Price objections are usually about perceived value, not actual cost. Try saying: 'I understand budget concerns. Let's look at the ROI of this solution...' Then demonstrate specific value points.",
            "For 'need to think about it' objections, say: 'I understand. To help you make your decision, what specific aspects do you need to consider?' This reveals the real objection."
        ],
        "products": [
            "When presenting our insurance products, focus on protection and peace of mind rather than focusing on negative scenarios. For example: 'This coverage ensures your family maintains their lifestyle, no matter what happens.'",
            "For investment products, use simple analogies to explain complex features. Compare SIPs to regular exercise - small, consistent actions that yield significant results over time.",
            "Cross-selling works best when you phrase it as enhancing their primary purchase: 'Many customers who get our loan protection also add this health cover to ensure complete financial security.'"
        ],
        "motivation": [
            "Try the 5-minute rule when you're feeling unmotivated. Tell yourself you'll work on just one sales activity for 5 minutes. Once you start, momentum usually keeps you going.",
            "Track your small wins daily. Even reaching out to 5 new prospects is progress worth celebrating.",
            "Remember, sales is a numbers game. Every 'no' gets you closer to a 'yes'. The top salespeople usually hear 'no' more times than average performers - they just make more attempts."
        ],
        "script": [
            "Instead of a rigid script, try a flexible framework:\n\n1. Personalized greeting\n2. Value statement (problem you solve)\n3. Qualifying questions\n4. Tailored solution\n5. Clear next step\n\nThis allows natural conversation while ensuring you cover key points.",
            "For cold calls, try: 'Hi [Name], I'm [Your Name] from GroMo. We help people like you [specific value proposition]. I'm curious - are you currently [question about problem your product solves]?'",
            "For follow-ups: 'Hi [Name], when we spoke last [specific reference to previous conversation], you mentioned [specific need/concern]. I've got some information about how we can address that. Do you have 5 minutes to discuss this now?'"
        ]
    }
    
    # Determine which category the input falls into
    if any(word in input_lower for word in ["hi", "hello", "hey", "greetings"]):
        category = "greeting"
    elif any(word in input_lower for word in ["close", "closing", "seal", "deal", "finalize"]):
        category = "closing"
    elif any(word in input_lower for word in ["objection", "refuse", "hesitate", "concern", "worry"]):
        category = "objection"
    elif any(word in input_lower for word in ["product", "offer", "insurance", "investment", "mutual", "fund"]):
        category = "products"
    elif any(word in input_lower for word in ["motivate", "motivation", "inspire", "energy", "tired", "burnout"]):
        category = "motivation"
    elif any(word in input_lower for word in ["script", "pitch", "presentation", "talk", "say"]):
        category = "script"
    else:
        # General advice for unmatched queries
        return "As a sales professional, remember that listening is often more important than talking. Ask open-ended questions to understand your customer's needs better, then tailor your solution to address their specific situation. Would you like more specific advice on a particular sales challenge?"
    
    # Return a random response from the matching category
    return random.choice(responses[category])

def get_sales_tip_of_the_day():
    """
    Return a daily sales tip
    
    Returns:
        str: Sales tip
    """
    tips = [
        "Listen more than you speak. Successful sales conversations should be 70% listening, 30% talking.",
        "Follow up persistently but respectfully. It takes an average of 8 touches to get a response from a new prospect.",
        "Use social proof. Share specific success stories similar to your prospect's situation.",
        "Learn to read buying signals. Questions about implementation, pricing details, or timing often indicate interest.",
        "Focus on solving problems, not pushing products. Customers buy solutions, not features.",
        "Practice empathy. Put yourself in your customer's position to understand their real concerns.",
        "Use the prospect's language. Note their terminology and mirror it in your responses.",
        "Prepare for common objections. Have clear, concise responses ready for price, timing, and need objections.",
        "Qualify leads thoroughly. Don't waste time on prospects who aren't a good fit.",
        "End each interaction with a clear next step that both parties agree on."
    ]
    
    # Use the day of year to select a tip, so it changes daily but is consistent throughout the day
    day_of_year = datetime.now().timetuple().tm_yday
    return tips[day_of_year % len(tips)]
