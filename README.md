Resume Skill Extractor

A simple web app built with Python and Streamlit that extracts text from resumes and compares it with job descriptions.

Features:

Extracts text from PDF resumes
Compares resume content with a given job description
Highlights matching and missing keywords
Generates structured results in CSV format
User-friendly Streamlit interface

Tech Stack:

Python 3
Streamlit – web app framework
PyPDF2 – extract text from PDF resumes
pandas – data handling

resume-skill-extractor/
│
├── resume_skill_extractor.py   # Main Streamlit app
├── requirements.txt            # Python dependencies
├── sample_resume.pdf           # Example resume (optional)
├── job_description.txt         # Example job description (optional)
└── README.md                   # Project documentation

Future Improvements:

Add skill extraction using NLP libraries
Support for DOCX resumes


