# LoveLink - Dating App

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

## 📚 API Documentation

### Authentication Endpoints

#### POST `/api/signup`

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword",
  "confirm_password": "securepassword"
}
```

**Response:**

```json
{
  "message": "Account created successfully!",
  "user_id": 1
}
```

#### POST `/api/login`

Authenticate user login.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "message": "Logged in successfully!",
  "user_id": 1
}
```

#### POST `/api/logout`

Logout current user.

**Response:**

```json
{
  "message": "Logged out successfully!"
}
```

### Profile Endpoints

#### GET `/api/profile`

Get current user's profile.

**Response:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "gender": "male",
  "bio": "Hello world!",
  "location": "New York",
  "occupation": "Developer",
  "education_level": "Bachelor's",
  "relationship_goal": "Long-term"
}
```

#### POST `/api/profile`

Update user profile.

**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated bio",
  "location": "New York"
}
```

### Other Endpoints

- `POST /api/upload-photo` - Upload profile picture
- `POST /api/password-reset` - Request password reset
- `GET/POST /api/preferences` - Manage match preferences
- `POST /api/message` - Send messages
- `POST /api/report` - Report users

## 🏗 Project Structure

```
├── app/                    # Flask backend
│   ├── __init__.py        # App factory
│   ├── model.py           # Database models
│   ├── forms.py           # WTForms
│   ├── views.py           # API routes
│   └── config.py          # Configuration
├── src/                    # Vue.js frontend
│   ├── views/             # Page components
│   ├── components/        # Reusable components
│   ├── router/            # Vue Router config
│   └── main.js            # App entry point
├── public/                 # Static assets
├── requirements.txt        # Python dependencies
└── package.json           # Node dependencies
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

## 📄 License

This project is licensed under the MIT License.
Set u
