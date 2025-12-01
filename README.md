Bloggers-Hub
A Django-based blogging platform with user accounts, email OTP verification, rich text editing, and REST API support.
This project uses Django 5.2+, a custom user model, CKEditor, Django-AllAuth, and Django REST Framework.

Features :-

Custom User Model (users.User)
Email-based OTP login (via EmailOTP model + SMTP)
Blog system with:
Authors
Upvotes
Rich-text editing (CKEditor)
REST API support (Django REST Framework)
Internationalization (English, Spanish, French)
Static/media asset handling
AllAuth user authentication
PostgreSQL support (default)

Tech Stack :-

Backend: Python, Django 5.2.2
Database: PostgreSQL (default) or SQLite (local)
Auth: Django AllAuth + Custom backend
Editors: CKEditor
API: Django REST Framework
Email: SMTP (Gmail example included)

Project Structure :-
myproj/
├─ manage.py
├─ myproj/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ users/
│  ├─ models.py       # Custom User, EmailOTP, UserProfile
│  ├─ views.py
│  ├─ utils.py        # OTP generation + email helpers
│  └─ migrations/
├─ blogs/
│  ├─ models.py       # Blog models with upvote system
│  └─ migrations/
├─ static/
├─ templates/
└─ media/

Contact

Maintainer: Ridhiman
GitHub: https://github.com/RidhimaN21
