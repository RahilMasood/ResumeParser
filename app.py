from flask import Flask, render_template, request, jsonify
import PyPDF2
import os
import tempfile
import requests
import re

app = Flask(__name__)

# OpenRouter configuration
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemini-2.0-flash-thinking-exp:free"

# Global variable to store the extracted resume text for the conversation context
resume_text = ""

def extract_text_from_pdfs(pdf_files):
    extracted_text = ""
    for pdf_file in pdf_files:
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"
        except Exception as e:
            extracted_text += f"Error extracting text from {pdf_file.filename}: {str(e)}\n"
    return extracted_text

def analyze_resume(extracted_text):
    global resume_text
    
    if not extracted_text.strip():
        return "No text could be extracted from the uploaded resume. Please ensure the file contains readable text."
    
    # Store the resume text for context in future conversations
    resume_text = extracted_text
    
    prompt = f"""
    You are CareerPulse, a career advisor AI. A user has uploaded their resume.
    Your job is to analyze it and provide career suggestions.
    
    Here is the full content of their resume:
    --- START RESUME TEXT ---
    {extracted_text}
    --- END RESUME TEXT ---
    
    Based on the resume, provide a friendly and detailed analysis including:
    1. A summary of their skills, experience, and qualifications
    2. Strong points in their profile and areas that could be improved
    3. 3-5 specific career paths that would be suitable for them based on their background
    4. Specific skills they could develop to enhance their career prospects
    5. Industries that might be particularly interested in their profile
    
    Be encouraging but realistic. Format your response in a clean, readable manner with clear sections. 
    Remember the text will displayed as showed so dont try to bold or italic or format it. Give plain text.
    """
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def generate_career_response(query):
    global resume_text
    
    # Check if the query contains the word "roast" (case insensitive)
    if re.search(r'\broast\b', query, re.IGNORECASE):
        prompt = f"""
        You are CareerPulse, a career advisor AI. The user has asked you to roast them based on their resume.
        Give a brutal but funny roast of their resume and career choices in slangs.
        Make it harsh but still somewhat constructive, focusing on resume red flags and career choices.
        
        Here is the resume content to roast:
        --- START RESUME TEXT ---
        {resume_text}
        --- END RESUME TEXT ---
        
        Be extra harsh, use slangs, and don't hold back. Make it sound like a comedy roast.
        Remember the text will displayed as showed so dont try to bold or italic or format it. Give plain text.
        """
    else:
        prompt = f'''
        You are CareerPulse, a career advisor AI. The user is having a conversation with you about their career.
        
        Here is their resume for context:
        --- START RESUME TEXT ---
        {resume_text}
        --- END RESUME TEXT ---
        
        Their question or comment is: "{query}"
        Provide helpful, personalized career advice based on their resume and current question.
        Be encouraging, specific, and actionable in your guidance.
        Remember the text will displayed as showed so dont try to bold or italic or format it. Give plain text.
        '''
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '')
    
    # If no resume has been uploaded yet
    if not resume_text:
        if "roast" in query.lower():
            return jsonify({'response': "I can't roast you until you upload your resume! Upload it first, then ask for a roast if you're brave enough."})
        else:
            return jsonify({'response': "Please upload your resume first so I can provide personalized career advice!"})
    
    response = generate_career_response(query)
    return jsonify({'response': response})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'response': 'No files uploaded'})
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({'response': 'No files selected'})
    
    # Process only PDF files
    pdf_files = [f for f in files if f.filename.lower().endswith('.pdf')]
    
    if not pdf_files:
        return jsonify({'response': 'No PDF resume was uploaded. Please upload your resume in PDF format.'})
    
    extracted_text = extract_text_from_pdfs(pdf_files)
    analysis = analyze_resume(extracted_text)
    
    return jsonify({'response': analysis})

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    global resume_text
    resume_text = ""
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
