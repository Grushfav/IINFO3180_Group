# DriftDater - Dating App
## INFO 3180 Group project

### Gavin Seaton 620043505 - Backend Lead
### Rayna Jarrett 620162148 - QA/Testing Lead 
### Shenelle Turner 620161664 - Frontend Lead
### Kaija Hall 620161114 - Project Manager

A modern dating application built with Vue.js 3 frontend and Flask REST API backend. Features user authentication, profiles, matching, messaging, and social features.

## 🚀 Features

- **User Authentication**: Secure signup/login with Flask-Login
- **User Profiles**: Comprehensive profile management with photos
- **Matching System**: Find compatible matches based on preferences; `GET /api/matches`, `GET /api/matches/potential`, and **`GET /api/users`** (search) include **`distance_km`** and **`distance_mi`** when both users have latitude/longitude set (null otherwise).
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

The API lives in **`backend/`** and the Vue app in **`frontend/`**. Run each from its own folder (two terminals).

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd INFO3180-MAIN-GROUP-PROJECT
   ```

2. **Create virtual environment** (from the repo root)

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies** (from **`backend/`**)

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Environment and database**

   Create **`backend/.env`** (optional but recommended) or set variables in your shell:

   ```bash
   FLASK_APP=app
   FLASK_DEBUG=1
   DATABASE_URL=postgresql://username:password@localhost:5432/dating_app
   SECRET_KEY=change-me-in-dev
   ```

   **Windows (PowerShell)** example:

   ```powershell
   cd backend
   $env:FLASK_APP = "app"
   $env:FLASK_DEBUG = "1"
   $env:DATABASE_URL = "postgresql://username:password@localhost:5432/dating_app"
   ```

   This repo already includes Alembic migrations under **`backend/migrations/`**. After PostgreSQL is running and `DATABASE_URL` points at your database:

   ```bash
   cd backend
   flask db upgrade
   ```

   Do **not** run `flask db init` unless you are replacing migrations from scratch (it will clash with the existing `migrations` folder).

5. **Run the Flask API**

   The frontend dev client defaults to **`http://localhost:8080`** (see `frontend/src/services/api.js`). Start Flask on that port:

   ```bash
   cd backend
   flask run --port 8080
   ```

   API base URL: **`http://localhost:8080`** (e.g. `http://localhost:8080/api/health`).

### Frontend Setup

1. **Install dependencies** (from **`frontend/`**)

   ```bash
   cd frontend
   npm install
   ```

   Axios is already listed in `package.json`; no separate install step is required.

2. **Optional: API URL override**

   If your API is not on port 8080, create **`frontend/.env`**:

   ```bash
   VITE_API_BASE_URL=http://localhost:5000
   ```

3. **Start the dev server**

   ```bash
   cd frontend
   npm run dev
   ```

   The app is served at **`http://localhost:5173`** (Vite default).

Register a new user account in the browser.

## Screenshots

### Sign up flow
![Sign up flow](frontend/src/assets/signup.png)
### Profile flow
![Profile flow](frontend/src/assets/profile.png)
### People near me
![People near me](frontend/src/assets/people_near_me.png)
### Matches
![User matches](frontend/src/assets/matches.png)
### Search
![Search](frontend/src/assets/search.png)
### Messages
![Messages](frontend/src/assets/message.png)
### Messages detail
![Messages detail](frontend/src/assets/messages3.png)


## 🏗 Project Structure

```
├── backend/
│   ├── app/                 # Flask application
│   │   ├── __init__.py      # App + extensions (db, login, CORS)
│   │   ├── config.py
│   │   ├── views.py         # REST routes
│   │   ├── model.py
│   │   ├── forms.py
│   │   ├── auth_token.py
│   │   └── static/uploads/  # Uploaded profile images
│   ├── migrations/          # Alembic / Flask-Migrate revisions
│   ├── requirements.txt
│   └── wsgi.py              # Gunicorn entry (e.g. Render)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/          # Pinia
│   │   └── services/       # Axios client + media URL helpers
│   ├── package.json
│   └── vite.config.js
├── render.yaml
└── README.md
```

## 🚀 Deployment

### Backend Deployment

From **`backend/`**, with `DATABASE_URL`, `SECRET_KEY`, and `CORS_ORIGINS` set for your environment:

```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:application
```

(On Render, use something like: `gunicorn --bind 0.0.0.0:$PORT wsgi:application` — see `render.yaml`.)

### Frontend Deployment

```bash
cd frontend
npm ci
npm run build
```

Deploy the **`frontend/dist/`** folder (static hosting). Set **`VITE_API_BASE_URL`** at build time to your public API URL.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📡 API Documentation

All endpoints are prefixed with `/api`. All request and response bodies use `application/json` unless stated otherwise. Endpoints marked 🔒 require an active login session.

---

### Health

#### `GET /api/health`
Check that the API is running.

**Response `200`**
```json
{ "message": "DriftDater API is running" }
```

---

### Authentication

#### `POST /api/signup`
Register a new user account. Also creates a minimal profile record.

**Request body**
| Field | Type | Required | Notes |
|---|---|---|---|
| `email` | string | ✅ | Must be unique |
| `username` | string | ✅ | Must be unique |
| `password` | string | ✅ | |
| `first_name` | string | ✅ | |
| `last_name` | string | ✅ | |
| `date_of_birth` | string | ✅ | Format: `YYYY-MM-DD` |
| `gender` | string | ✅ | e.g. `"male"`, `"female"`, `"non-binary"`, `"other"` |
| `looking_for` | string | | `"male"`, `"female"`, or `"any"` (default) |

**Response `201`**
```json
{ "message": "Account created successfully!", "user_id": 1 }
```

**Response `400`** — validation errors
```json
{ "errors": ["Error in the Email field - Invalid email address"] }
```

**Response `409`** — duplicate email or username
```json
{ "errors": ["Email or username already exists"] }
```

---

#### `POST /api/login`
Log in with email and password.

**Request body**
| Field | Type | Required |
|---|---|---|
| `email` | string | ✅ |
| `password` | string | ✅ |
| `remember` | boolean | |

**Response `200`**
```json
{ "message": "Logged in successfully!", "user_id": 1 }
```

**Response `401`**
```json
{ "error": "Invalid email or password" }
```

---

#### `POST /api/logout` 🔒
Log out the current user.

**Response `200`**
```json
{ "message": "Logged out successfully!" }
```

---

### Profile

#### `GET /api/profile` 🔒
Get the current logged-in user's full profile.

**Response `200`**
```json
{
  "id": 1,
  "user_id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Wonder",
  "date_of_birth": "1999-03-14",
  "age": 26,
  "gender": "female",
  "looking_for": "any",
  "bio": "Love hiking and adventure!",
  "location": "Kingston, Jamaica",
  "profile_photo": "user_1_profile.jpg",
  "occupation": "Software Developer",
  "education_level": "bachelors",
  "height_cm": 165,
  "relationship_goal": "long-term",
  "preferred_min_age": 22,
  "preferred_max_age": 35,
  "max_distance_km": 50,
  "latitude": 17.9970,
  "longitude": -76.7936,
  "interests": ["hiking", "music", "cooking"],
  "is_public": true
}
```

---

#### `POST /api/profile` 🔒
Update the current user's profile.

**Request body** *(all fields optional)*
| Field | Type | Notes |
|---|---|---|
| `first_name` | string | |
| `last_name` | string | |
| `date_of_birth` | string | Format: `YYYY-MM-DD` |
| `gender` | string | |
| `looking_for` | string | |
| `bio` | string | |
| `location` | string | |
| `occupation` | string | |
| `education_level` | string | |
| `relationship_goal` | string | |
| `preferred_min_age` | integer | |
| `preferred_max_age` | integer | Must be ≥ `preferred_min_age` |
| `max_distance_km` | integer | |
| `latitude` | float | |
| `longitude` | float | |
| `is_public` | boolean | |
| `interests` | array of strings | Minimum 3 required if included |

**Response `200`**
```json
{ "message": "Profile updated successfully!" }
```

**Response `400`** — e.g. fewer than 3 interests
```json
{ "errors": ["Please add at least 3 interests"] }
```

---

#### `POST /api/upload-photo` 🔒
Upload a profile photo. Send as `multipart/form-data`.

**Form field**
| Field | Type | Notes |
|---|---|---|
| `photo` | file | Allowed types: `png`, `jpg`, `jpeg`, `gif`, `webp` |

**Response `200`**
```json
{
  "message": "Photo uploaded successfully!",
  "photo_url": "/static/uploads/user_1_profile.jpg"
}
```

**Response `400`**
```json
{ "errors": ["File type not allowed"] }
```

---

### Users (Browse & Search)

#### `GET /api/users` 🔒
Browse and search public profiles. Excludes the current user.

**Query parameters**
| Param | Type | Notes |
|---|---|---|
| `name` | string | Searches first name, last name, and bio |
| `location` | string | Partial match |
| `gender` | string | Exact match |
| `age_min` | integer | |
| `age_max` | integer | |
| `interests` | string | Comma-separated list e.g. `"hiking,music"` |
| `sort_by` | string | `newest` (default), `age_asc`, `age_desc`, `name_asc` |

**Response `200`** — array of profile objects (same shape as `GET /api/profile`)

---

#### `GET /api/users/:user_id` 🔒
Get a specific user's public profile.

**Response `200`** — profile object

**Response `403`**
```json
{ "error": "Profile is private" }
```

**Response `404`**
```json
{ "error": "User not found" }
```

---

### Matching

#### `GET /api/matches` 🔒
Get all mutual matches (both users liked each other).

**Response `200`**
```json
[
  {
    "id": 5,
    "matched_at": "2025-04-10T14:32:00",
    "user": { "...profile object..." }
  }
]
```

---

#### `GET /api/matches/potential` 🔒
Get suggested profiles the current user has not yet liked or passed. Sorted by match score.

Matching factors (scored out of 100):
- Shared interests — up to 60 points
- Distance closeness — up to 25 points
- Relationship goal compatibility — up to 15 points

Also filters by gender preference, preferred age range, and max distance radius (when coordinates are available).

**Response `200`** — array of profile objects, each with an added `match_score` field
```json
[
  {
    "id": 2,
    "first_name": "Grace",
    "match_score": 78,
    "..."
  }
]
```

---

#### `POST /api/matches/like/:user_id` 🔒
Like another user. If they have already liked the current user, both match records are updated to `"matched"`.

**Response `200`** — already liked previously
```json
{ "message": "Already liked" }
```

**Response `200`** — new like, no mutual match yet
```json
{ "message": "Liked!", "matched": false }
```

**Response `200`** — mutual match created
```json
{ "message": "Matched!", "matched": true }
```

**Response `400`**
```json
{ "error": "Cannot like yourself" }
```

---

#### `POST /api/matches/pass/:user_id` 🔒
Pass on a user so they no longer appear in potential matches.

**Response `200`**
```json
{ "message": "Passed" }
```

---

### Messages

#### `GET /api/messages` 🔒
Get all conversations — one entry per mutual match, showing the latest message.

**Response `200`**
```json
[
  {
    "id": 5,
    "user": { "...profile object..." },
    "last_message": "Hey, how are you?",
    "last_message_at": "2025-04-11T09:15:00",
    "unread": 0
  }
]
```

---

#### `GET /api/messages/:user_id` 🔒
Get the full message history between the current user and a matched user.

**Response `200`**
```json
[
  {
    "id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "content": "Hey, how are you?",
    "created_at": "2025-04-11T09:15:00",
    "edited": false
  }
]
```

**Response `403`** — users are not mutually matched
```json
{ "error": "No match found with this user" }
```

---

#### `POST /api/messages/:user_id` 🔒
Send a message to a matched user.

**Request body**
| Field | Type | Required |
|---|---|---|
| `content` | string | ✅ |

**Response `201`**
```json
{
  "id": 42,
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Hey, how are you?",
  "created_at": "2025-04-11T09:15:00",
  "edited": false
}
```

**Response `403`** — not matched with this user
```json
{ "error": "You can only message your matches" }
```

**Response `400`**
```json
{ "errors": ["Message cannot be empty"] }
```

---

### Favourites

#### `GET /api/favourites` 🔒
Get all profiles the current user has saved.

**Response `200`** — array of profile objects

---

#### `POST /api/favourites/:profile_id` 🔒
Save a profile to favourites.

**Response `201`**
```json
{ "message": "Saved to favourites" }
```

**Response `200`** — already saved
```json
{ "message": "Already saved" }
```

---

#### `DELETE /api/favourites/:profile_id` 🔒
Remove a profile from favourites.

**Response `200`**
```json
{ "message": "Removed from favourites" }
```

---

## ⚠️ Known Issues & Limitations

### `pass` status stored as `"blocked"`
The `POST /api/matches/pass/:user_id` endpoint in `views.py` assigns a match status of `"blocked"` instead of `"passed"`. This means that the database system treats passed users and blocked users as identical entities. If in the future the system requires the block/report feature, it will need to be separated into distinct statuses.

### Age filtering happens in Python, not SQL
Both `GET /api/users` and `GET /api/matches/potential` use age range filtering which operates through Python list comprehension after the database query execution. Since age is calculated from `date_of_birth` rather than stored as a column, the full result set is loaded into memory before filtering. This will result in slower response times when there is a large number of users.

### Potential matches capped at 20
The `GET /api/matches/potential` endpoint applies `.limit(20)` before age and distance filtering. After those filters are applied, fewer than 20 results may be returned — sometimes significantly fewer if a user has strict preferences. This limit should be applied after all filtering, not before.

### No pagination
`GET /api/users` and `GET /api/matches` return all results in a single response. This will become a performance issue as the number of users grows. Adding `page` and `per_page` query parameters would address this.

### Profile photo is overwritten on re-upload
`POST /api/upload-photo` uses the format `user_{id}_profile.{ext}` to name its uploaded files. The system allows users to upload different file types yet it continues to store the original file under its previous name which results in storage waste.

### No CSRF protection on API routes
All routes disable CSRF with `meta={'csrf': False}`. This is acceptable for a session-cookie API only if the frontend is served from the same origin. If the frontend and backend are ever hosted on separate domains, this should be revisited.