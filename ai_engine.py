import streamlit as st
import requests
import json

def get_ai_strategy(student_name, persona, accuracy, hints):
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # Using the absolute STABLE v1 endpoint to avoid the 404 v1beta error
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt_text = f"""
    Analyze this student as a pedagogical expert:
    Name: {student_name}
    Behavioral Persona: {persona}
    Accuracy: {accuracy}%
    Hints: {hints}
    
    Provide 3 tactical coaching tips for the teacher.
    """
    
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        if response.status_code == 200:
            # Extracting the text from the standard Google JSON response
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ API Error {response.status_code}: {response_data.get('error', {}).get('message', 'Unknown Error')}"
            
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"