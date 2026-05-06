# DriftDater - Dating App
## INFO 3180 Group project

### Gavin Seaton 620043505
### Rayna Jarrett 620162148
### Shenelle Turner 620161664
### Kaija Hall 

A modern dating application built with Vue.js 3 frontend and Flask REST API backend. Features user authentication, profiles, matching, messaging, and social features.

## 🚀 Features

- **User Authentication**: Secure signup/login with Flask-Login
- **User Profiles**: Comprehensive profile management with photos
- **Matching System**: Find compatible matches based on preferences
- **Real-time Messaging**: Chat with matches
- **Photo Uploads**: Profile picture management
- **Responsive Design**: Mobile-friendly Vue.js interface

## 🛠 Tech Stack

### Backend

- **Flask** - Python web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Migrate** - Database migrations
- **Flask-Login** - User authentication
- **Flask-WTF** - Form handling
- **PostgreSQL** - Database

### Frontend

- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Single-page application routing
- **Axios** - HTTP client for API calls
- **Vite** - Fast build tool

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database

## 🔧 Installation & Setup

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd INFO3180-MAIN-GROUP-PROJECT
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**

   ```bash
   # Set environment variables (create .env file)
   export FLASK_APP=app
   export FLASK_ENV=development
   export DATABASE_URL=postgresql://username:password@localhost/dating_app

   # Initialize database
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run Flask API**
   ```bash
   flask run
   ```
   API will be available at `http://localhost:5000`

### Frontend Setup

1. **Install Node dependencies**

   ```bash
   npm install
   ```

2. **Install Axios for API calls**

   ```bash
   npm install axios
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`


Register a new user account.

## Screenshots

### Sign up flow
![Sign up flow](src/assets/signup.png)
### Profile flow
![Profile flow](src/assets/profile.png)
### People near me
![People near me](src/assets/people_near_me.png)
### Matches
![User matches](src/assets/matches.png)
### Search
![Search](src/assets/search.png)
### Messages
![Messages](src/assets/message.png)
### Messages detail
![Messages detail](src/assets/messages3.png)


## 🏗 Project Structure

```
├── app/                 # Flask application
│   ├── __init__.py      # App + extensions (db, login, CORS)
│   ├── config.py        # Settings from environment
│   ├── views.py         # REST routes
│   ├── model.py         # SQLAlchemy models
│   ├── forms.py         # WTForms validation
│   └── static/uploads/  # Uploaded profile images (gitignored in practice)
├── migrations/          # Alembic / Flask-Migrate revisions
├── src/                 # Vue 3 SPA
│   ├── components/
│   ├── views/
│   ├── router/
│   ├── stores/          # Pinia
│   └── services/        # Axios client + media URL helpers
├── requirements.txt
├── package.json
└── README.md
```

## 🚀 Deployment

### Backend Deployment

```bash
# Production settings
export FLASK_ENV=production
export DATABASE_URL=your_production_db_url

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Frontend Deployment

```bash
npm run build
# Deploy dist/ folder to your web server
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

