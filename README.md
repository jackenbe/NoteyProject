# 📝 Notey Notebook

**Notey Notebook** is a web-based academic note-sharing and personal note-taking platform tailored for college students. Built using Django, it enables users to create, manage, and share course-related notes by university and class, promoting collaborative learning beyond institutional boundaries.

## 🔗 Live Preview
https://notey-project.onrender.com/

---

## 🚀 Features

- ✅ User authentication and registration with university affiliation
- 🏫 Join and view groups tied to universities
- 📓 Create personal and group notes (public/private)
- 📝 Edit/delete your notes
- 👍 Vote on public notes (upvote/downvote)
- 💬 Comment on group notes with threaded replies
- 🔍 Real-time search across notes
- ⭐ Favorite notes for quick access
---

## 🛠️ Tech Stack

| Layer       | Technology                   |
|------------|------------------------------|
| Frontend    | HTML, CSS (Bootstrap 5), Django templates |
| Backend     | Django (Python),  PostgresSQL)         |
| Authentication | Django Auth System |
| Architecture | MVC (Model-View-Controller) via Django |
| Deployment | render |
---

## 📁 Project Structure
```text
Notey/
├── Notey/                     # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                      # Main application logic
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── form.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/
│
├── manage.py
├── requirements.txt
└── .gitignore
```
---

## 🚀 Features

- ✅ University-based registration
- 🔐 Login/Logout system
- 🏫 Join study groups via invite codes
- 📓 Create group and personal notes (public/private)
- ✏️ Edit & delete your own notes
- 💬 Comment on shared notes
- 👍 Upvote/downvote notes
- ⭐ Favorite notes for easy access
- 🔍 Search notes by keystroke
- 📁 Organize notes by course

---

## 🛠️ Tech Stack

| Layer        | Tech                          |
|--------------|-------------------------------|
| Framework    | Django (Python)               |
| Forms        | Django Forms                  |
| Frontend     | HTML + Bootstrap 5            |
| Auth         | Django Auth System            |
| Database     | SQLite (default, switchable)  |
| Templates    | Django Templating Engine      |

---

## 🔐 User Roles & Permissions

- **Authenticated users**:
  - Can join universities/groups
  - Can create/edit/delete personal & group notes
  - Can vote/comment on public group notes
- **Note authors/group creators**:
  - Have full control over their notes and groups
- **Unauthorized users**:
  - Redirected to login when trying to access restricted views

---

## 💻 Local Development

### Prerequisites

- Python 3.10+
- Virtualenv or venv
- Git

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/notey.git
cd notey

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Run development server
python manage.py runserver
