from flask import Flask, request, jsonify, render_template, send_from_directory
import google.generativeai as genai
import pypdf
import io
import os
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY environment variable is required")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def read_pdf(file):
    """Reads text from a PDF file."""
    text = ""
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text()
        if not text.strip():
            logger.warning("PDF file is empty or contains no text")
            return None
        return text
    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}")
        return None

def analyze_resume(pdf_text, analysis_option, job_description):
    try:
        if analysis_option == "Quick Scan":
            prompt = f"""
            You are ResumeChecker, an expert in resume analysis. Provide a quick scan of the following resume:

            1. Identify the most suitable profession for this resume.
            2. List 3 key strengths of the resume.
            3. Suggest 2 quick improvements.
            4. Give an overall ATS score out of 100.

            Resume text: {pdf_text}
            Job description (if provided): {job_description}
            """
        elif analysis_option == "Detailed Analysis":
            prompt = f"""
            You are ResumeChecker, an expert in resume analysis. Provide a detailed analysis of the following resume:

            1. Identify the most suitable profession for this resume.
            2. List 5 strengths of the resume.
            3. Suggest 3-5 areas for improvement with specific recommendations.
            4. Rate the following aspects out of 10: Impact, Brevity, Style, Structure, Skills.
            5. Provide a brief review of each major section (e.g., Summary, Experience, Education).
            6. Give an overall ATS score out of 100 with a breakdown of the scoring.

            Resume text: {pdf_text}
            Job description (if provided): {job_description}
            """
        else:  # ATS Optimization
            prompt = f"""
            You are ResumeChecker, an expert in ATS optimization. Analyze the following resume and provide optimization suggestions:

            1. Identify keywords from the job description that should be included in the resume.
            2. Suggest reformatting or restructuring to improve ATS readability.
            3. Recommend changes to improve keyword density without keyword stuffing.
            4. Provide 3-5 bullet points on how to tailor this resume for the specific job description.
            5. Give an ATS compatibility score out of 100 and explain how to improve it.

            Resume text: {pdf_text}
            Job description: {job_description}
            """

        response = model.generate_content(prompt)
        if not response or not response.text:
            logger.error("Empty response from Gemini API")
            return "Error: Failed to generate analysis. Please try again."
        return response.text
    except Exception as e:
        logger.error(f"Error in analyze_resume: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        pdf_text = read_pdf(file)
        if pdf_text is None:
            return jsonify({'error': 'Failed to read PDF. Please ensure it contains text and is not corrupted.'}), 400

        analysis_option = request.form.get('analysis_type', 'Quick Scan')
        job_description = request.form.get('job_description', '')

        analysis = analyze_resume(pdf_text, analysis_option, job_description)
        if analysis.startswith('Error:'):
            return jsonify({'error': analysis}), 500

        return jsonify({'analysis': analysis})
    except Exception as e:
        logger.error(f"Error in api_analyze: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.json
        message = data.get('message')
        analysis = data.get('analysis')

        if not message or not analysis:
            return jsonify({'error': 'Missing required fields'}), 400

        chat_prompt = f"""
        You are an assistant answering questions about the following resume analysis:

        {analysis}

        User's question: {message}
        """

        response = model.generate_content(chat_prompt)
        if not response or not response.text:
            return jsonify({'error': 'Failed to generate response'}), 500

        return jsonify({'response': response.text})
    except Exception as e:
        logger.error(f"Error in api_chat: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)