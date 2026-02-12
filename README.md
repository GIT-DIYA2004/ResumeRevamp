# ResumeRevamp - AI Resume Analysis Tool

ResumeRevamp is an AI-powered resume analysis tool that helps you optimize your resume for job applications. It uses Google's Gemini AI to provide detailed analysis and suggestions for improvement.

## Features

- PDF Resume Analysis
- Multiple Analysis Types:
  - Quick Scan
  - Detailed Analysis
  - ATS Optimization
- Interactive Chat Interface
- Job Description Integration
- Modern, Responsive UI

## Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini AI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resumerevamp
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload your resume (PDF format) and optionally provide a job description.

4. Select the type of analysis you want:
   - Quick Scan: Basic analysis with key points
   - Detailed Analysis: Comprehensive review with ratings
   - ATS Optimization: Focus on ATS compatibility

5. Click "Analyze Resume" to get started.

6. Use the chat interface to ask questions about the analysis.

## Project Structure

```
resumerevamp/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Stylesheets
│   └── js/
│       └── main.js    # Frontend JavaScript
├── templates/
│   └── index.html     # Main HTML template
└── uploads/           # Temporary storage for uploaded files
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 