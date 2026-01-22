# TicketDesk — Flask Ticket Management App

TicketDesk is a full-stack Flask web application that demonstrates user authentication,
CRUD functionality, and a modern UI. This project was built to showcase real-world
backend and frontend integration using Python.

## 🔗 Live Demo
_(Coming soon)_

## ✨ Features
- User registration, login, and logout (Flask-Login)
- Secure password hashing (Werkzeug)
- Create, edit, and delete tickets
- Ticket severity levels (Low, Medium, High, Critical)
- SQLite database with SQLAlchemy ORM
- REST-style JSON API endpoint
- Flash/toast notifications
- Delete confirmation modal
- Responsive UI with Bootstrap 5 + Icons

## 🧰 Tech Stack
- **Language:** Python  
- **Framework:** Flask  
- **Auth:** Flask-Login  
- **Database:** SQLite  
- **ORM:** SQLAlchemy  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5  
- **Version Control:** Git & GitHub  

## 🚀 Getting Started (Local Setup)

```bash
git clone https://github.com/YOUR-USERNAME/ticketdesk.git
cd ticketdesk
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
