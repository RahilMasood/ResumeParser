# 📝 Resume Parser

A simple and efficient resume parser web app built with **Flask**, created by **Rahil Masood** and **Rajarshi**. This tool extracts and displays relevant information from uploaded resumes to help recruiters or HR systems quickly analyze candidate details.

## 🚀 Features

- Upload resumes in common formats
- Automatically extract:
  - Name
  - Email
  - Phone Number
  - Skills
  - Education
  - Experience
- 
- Clean and responsive web interface
- Easy to deploy on local or cloud environments

## 🧠 Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML (Jinja2 templating)
- **Deployment:** Compatible with Render, Heroku, etc.

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/resume_parser.git
   cd resume_parser
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
3. **Run the app**
    ```bash
   # For PowerShell
    $env:FLASK_APP = "app.py"
    python -m flask run
4. **Visit Open your browser and go to: http://localhost:5000**

## 📁 Project Structure
    ```bash
    resume_parser/
    │
    ├── app.py                 # Main Flask app
    ├── requirements.txt       # Dependencies
    ├── render.yaml            # Deployment configuration (optional)
    └── templates/
        └── index.html         # Frontend UI

## 🙌 Authors

- [**Rahil Masood**](https://github.com/RahilMasood)
- [**Rajarshi**](https://github.com/<RajarshiUsername>)
