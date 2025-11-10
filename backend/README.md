# VocabKo Backend - Python FastAPI

Modern, async Python backend for the VocabKo Korean Vocabulary Learning Platform.

## 🚀 Technology Stack

- **Framework**: FastAPI 0.104+
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **Validation**: Pydantic V2
- **Language**: Python 3.10+

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── users.py         # User management
│   │   │   │   ├── flashcards.py    # Flashcard CRUD
│   │   │   │   └── quiz.py          # Quiz functionality
│   │   │   └── router.py            # API router
│   │   └── dependencies.py          # JWT auth dependency
│   ├── core/
│   │   ├── config.py                # Configuration
│   │   ├── database.py              # MongoDB connection
│   │   └── security.py              # JWT & password hashing
│   └── models/
│       ├── user.py                  # User models
│       ├── flashcard.py             # Flashcard models
│       └── quiz.py                  # Quiz models
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
└── .env.example                     # Environment variables template
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- MongoDB (local or MongoDB Atlas)

### Step 1: Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create `.env` file in the `backend/` directory:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=vocabko
SECRET_KEY=your-super-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DEBUG=True
```

### Step 4: Start MongoDB

**Option A: Local MongoDB**
```bash
mongod
```

**Option B: MongoDB Atlas (Cloud)**
- Create account at mongodb.com/atlas
- Create cluster and get connection string
- Update `MONGODB_URL` in `.env`

### Step 5: Run the Backend

```bash
# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use Python directly
python main.py
```

The API will be available at:
- **API Base**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username_or_email": "johndoe",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Users (Requires Authentication)

All user endpoints require `Authorization: Bearer <token>` header.

#### Get Current User Profile
```http
GET /api/v1/users/me
Authorization: Bearer <your_token>
```

#### Update Profile
```http
PUT /api/v1/users/me
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "daily_goal": 30,
  "username": "newusername"
}
```

#### Get User Stats
```http
GET /api/v1/users/stats
Authorization: Bearer <your_token>
```

### Flashcards

#### Get All Flashcards
```http
GET /api/v1/flashcards?skip=0&limit=50
Authorization: Bearer <your_token>
```

#### Get Specific Flashcard
```http
GET /api/v1/flashcards/{flashcard_id}
Authorization: Bearer <your_token>
```

#### Seed Sample Flashcards (Development)
```http
POST /api/v1/flashcards/seed
```

#### Update Progress
```http
POST /api/v1/flashcards/progress
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "flashcard_id": "507f1f77bcf86cd799439011",
  "known": true,
  "review_later": false
}
```

#### Get My Progress
```http
GET /api/v1/flashcards/progress/my
Authorization: Bearer <your_token>
```

### Quiz

#### Get Quiz Questions
```http
GET /api/v1/quiz/questions?count=20
Authorization: Bearer <your_token>
```

#### Submit Quiz
```http
POST /api/v1/quiz/submit
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "answers": [
    {
      "question": "안녕하세요",
      "user_answer": "Hello",
      "correct_answer": "Hello"
    }
  ]
}
```

#### Get Quiz Results
```http
GET /api/v1/quiz/results?skip=0&limit=10
Authorization: Bearer <your_token>
```

#### Get Quiz Statistics
```http
GET /api/v1/quiz/stats
Authorization: Bearer <your_token>
```

## 🗄️ Database Models

### User Collection
```json
{
  "_id": "ObjectId",
  "username": "string",
  "email": "string",
  "hashed_password": "string",
  "profile_picture": "string",
  "level": "string",
  "daily_goal": "number",
  "words_learned": "number",
  "study_streak": "number",
  "achievements": ["string"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Flashcard Collection
```json
{
  "_id": "ObjectId",
  "korean": "string",
  "english": "string",
  "example_korean": "string",
  "example_english": "string",
  "category": "string",
  "difficulty": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### User Progress Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "flashcard_id": "string",
  "known": "boolean",
  "review_later": "boolean",
  "times_reviewed": "number",
  "last_reviewed_at": "datetime",
  "accuracy": "number"
}
```

### Quiz Result Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "score": "number",
  "total_questions": "number",
  "correct_answers": "number",
  "incorrect_answers": "number",
  "answers": ["object"],
  "completed_at": "datetime"
}
```

## 🔐 Authentication Flow

1. **Register**: POST to `/api/v1/auth/register`
2. **Login**: POST to `/api/v1/auth/login` → Receive JWT token
3. **Use Token**: Include in `Authorization: Bearer <token>` header for protected endpoints
4. **Token Expiry**: Tokens expire after 7 days (configurable)

## 🧪 Testing with Swagger UI

1. Start the backend
2. Navigate to http://localhost:8000/docs
3. Click "Authorize" button
4. Enter token in format: `Bearer your_token_here`
5. Try out endpoints interactively

## 📦 Seeding Database

To populate the database with sample flashcards:

```bash
curl -X POST http://localhost:8000/api/v1/flashcards/seed
```

## 🚀 Production Deployment

### Using Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables for Production

```env
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/
DATABASE_NAME=vocabko_prod
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
```

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongosh

# Or check MongoDB service
sudo systemctl status mongod
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Errors
- Update `CORS_ORIGINS` in `app/core/config.py` to include your frontend URL

## 📝 License

MIT License

## 👨‍💻 Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Format code
black .

# Lint code
flake8 .
```

---

**Happy Coding! 🎉**
