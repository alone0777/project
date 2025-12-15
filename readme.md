# Mentor–Mentee Secure Web Application

This project is a Mentor–Mentee web application developed using Flask and MySQL.
The primary focus of the project on web application security by identifying common vulnerabilities (such as SQL Injection, Cross-Site Scripting, and insecure session handling) and mitigating them.
The application highlights how security can be integrated into a traditional web application without affecting its usability or functionality.

# Features and Security Objectives

## Core Functional Features
User registration for mentors and mentees
Secure login and role-based access control
Mentor approval  (admin-controlled)
Public messaging system with interest/expertise filtering
Mentor and mentee profile management
Admin dashboard for user oversight

## Security Objectives and Improvements
SQL Injection Prevention using SQLAlchemy ORM and parameterised queries
Cross-Site Scripting (XSS) Mitigation using input sanitisation (bleach) and safe template rendering
Secure Session Management using Flask sessions
Static Application Security Testing (SAST) using Bandit

## Project Structure

```text
project/
├── Admin/
│   ├── __init__.py          # Marks Admin as a package
│   ├── routes.py            # Admin-related routes and access control
│   ├── logic.py             # Admin business logic
│   └── templates/
│       └── *.html           # Jinja2 templates for admin views
│
├── mentor/
│   ├── __init__.py          # Mentor package initialization
│   ├── routes.py            # Mentor routes
│   ├── logic.py             # Mentor business logic
│   └── templates/
│       └── *.html           # Mentor templates
│
├── mentee/
│   ├── __init__.py          # Mentee package initialization
│   ├── routes.py            # Mentee routes and message handling
│   ├── logic.py             # Mentee business logic
│   └── templates/
│       └── *.html           # Mentee templates
│
├── config/
│   ├── config.py            # Database setup, SQLAlchemy init, security helpers
│   └── model.py             # SQLAlchemy models (User, Profiles, Messages)
│
├── templates/
│   └── *.html               # Shared Jinja2 templates
│
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

# Setup and Installation Instructions

Prerequisites
Python 3.10+
MySQL Server
Virtual environment (recommended)
Installation Steps

# Clone the repository
git clone https://github.com/alone0777/project.git
cd project

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt


# Run the Application
python main.py
The application will be available at:
https://127.0.0.1:5000

# Usage Guidelines
Register as a mentor or mentee
Login with your credentials
Mentors require admin approval before accessing full features
Mentees can post public messages based on interests
Mentors can filter and respond to messages based on expertise
Admin users manage approvals and system oversight
Note: Unauthorized access attempts are redirected to an access-denied page.

# Security Improvements Implemented
Parameterised database access via SQLAlchemy ORM
Input sanitisation using Bleach
Secure session handling using Flask’s session management
Role-based route protection
Reduced attack surface by limiting debug exposure
Centralised database and security configuration
These improvements significantly reduce risks associated with:
SQL Injection
XSS
Broken Access Control
Session Fixation
Testing Process
The application underwent both Functional Testing and Static Application Security Testing (SAST).

# Tools Used
Bandit – Static analysis for Python security issues
Manual test cases for authentication, authorization, and input handling

# Key Findings
Identification of hardcoded secrets and debug configurations
Validation of SQL injection and XSS mitigations
Review of session handling and role enforcement
Testing results and screenshots are documented in the Appendices section of the technical report.

# Contributions and References
## Frameworks and Libraries
Flask
Flask-SQLAlchemy
PyMySQL
Bleach
Bandit

## References
OWASP Top 10 Web Application Security Risks
Flask Official Documentation
Bandit Documentation
