import json
import requests
import streamlit as st

def load_lottieurl(url: str):
    """
    Load a Lottie animation from a URL
    
    Args:
        url (str): URL to the Lottie animation JSON
        
    Returns:
        dict: Lottie animation as a JSON object
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return get_fallback_animation()
        return r.json()
    except Exception as e:
        print(f"Error loading Lottie URL: {e}")
        return get_fallback_animation()
        
def get_fallback_animation():
    """
    Return a simple fallback animation when URL loading fails
    
    Returns:
        dict: Simple Lottie animation as a JSON object
    """
    return {
        "v": "5.7.1",
        "fr": 30,
        "ip": 0,
        "op": 60,
        "w": 200,
        "h": 200,
        "nm": "Simple Animation",
        "ddd": 0,
        "assets": [],
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "Shape Layer",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100},
                    "r": {
                        "a": 1,
                        "k": [
                            {"t": 0, "s": [0], "e": [360]},
                            {"t": 60, "s": [360]}
                        ]
                    },
                    "p": {"a": 0, "k": [100, 100]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "shapes": [
                    {
                        "ty": "rc",
                        "d": 1,
                        "s": {"a": 0, "k": [50, 50]},
                        "p": {"a": 0, "k": [0, 0]},
                        "r": {"a": 0, "k": 10}
                    },
                    {
                        "ty": "fl",
                        "c": {"a": 0, "k": [0.29, 0.78, 0.31, 1]},
                        "o": {"a": 0, "k": 100}
                    }
                ]
            }
        ]
    }

def load_lottiefile(filepath: str):
    """
    Load a Lottie animation from a file
    
    Args:
        filepath (str): Path to the Lottie animation JSON file
        
    Returns:
        dict: Lottie animation as a JSON object
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading Lottie file: {e}")
        return None

# Define a dictionary of commonly used animations
COMMON_ANIMATIONS = {
    'sales_dashboard': 'https://assets5.lottiefiles.com/packages/lf20_w4f2qg8o.json',
    'sales_coach': 'https://assets4.lottiefiles.com/private_files/lf30_dln2gqhg.json',
    'product_suggestions': 'https://assets6.lottiefiles.com/packages/lf20_uzvwjpkq.json',
    'performance': 'https://assets9.lottiefiles.com/packages/lf20_tllkbdio.json',
    'loading': 'https://assets3.lottiefiles.com/packages/lf20_b88nh30c.json',
    'success': 'https://assets1.lottiefiles.com/packages/lf20_ydo1amjm.json',
}

def get_animation(key):
    """
    Get a predefined animation by key
    
    Args:
        key (str): Key for the predefined animation
        
    Returns:
        dict: Lottie animation as a JSON object
    """
    if key in COMMON_ANIMATIONS:
        return load_lottieurl(COMMON_ANIMATIONS[key])
    return None
