# VocabKo - Full Stack Application

Complete Korean Vocabulary Learning Platform with Python FastAPI backend and Next.js frontend.

## 🎯 Architecture Overview

### Backend: Python FastAPI
- **Framework**: FastAPI (async, modern Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT tokens with python-jose
- **API Documentation**: Auto-generated Swagger UI

### Frontend: Next.js
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks + Context API

## 📁 Project Structure

```
FlashCard/
├── backend/                   # Python FastAPI Backend
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/     # API routes
│   │   │   └── router.py
│   │   ├── core/              # Config, database, security
│   │   └── models/            # Pydantic models
│   ├── main.py                # FastAPI app
│   ├── requirements.txt       # Python dependencies
│   └── README.md
│
├── frontend/                  # Next.js Frontend
│   ├── app/                   # Next.js 14 app directory
│   ├── components/            # React components
│   ├── lib/                   # Utilities & API client
│   ├── package.json
│   └── README.md
│
└── FULL_STACK_README.md       # This file
```

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URL and secret key

# Run backend
uvicorn main:app --reload
```

Backend will run on: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# Run development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users (Protected)
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/stats` - Get learning statistics

### Flashcards (Protected)
- `GET /api/v1/flashcards` - List flashcards
- `GET /api/v1/flashcards/{id}` - Get flashcard details
- `POST /api/v1/flashcards/seed` - Seed sample data
- `POST /api/v1/flashcards/progress` - Update learning progress
- `GET /api/v1/flashcards/progress/my` - Get my progress

### Quiz (Protected)
- `GET /api/v1/quiz/questions` - Get random quiz questions
- `POST /api/v1/quiz/submit` - Submit quiz answers
- `GET /api/v1/quiz/results` - Get quiz history
- `GET /api/v1/quiz/stats` - Get quiz statistics

## 🗄️ Database Collections

### users
- User accounts with profile info
- Learning statistics and streaks
- Achievements

### flashcards
- Korean/English vocabulary pairs
- Example sentences
- Categories and difficulty levels

### user_progress
- Individual flashcard progress
- Known/review later flags
- Review history

### quiz_results
- Quiz attempts and scores
- Detailed answer history
- Performance analytics

## 🔐 Authentication Flow

1. **Register**: User creates account
2. **Login**: User receives JWT token
3. **Store Token**: Frontend stores in localStorage/cookies
4. **Protected Requests**: Include `Authorization: Bearer <token>` header
5. **Token Expiry**: Tokens valid for 7 days

## 🎨 Frontend Features

- **Dashboard**: Overview of learning progress
- **Flashcards**: Interactive flip cards with audio
- **Quiz**: Multiple-choice questions
- **Progress**: Charts and statistics
- **Profile**: User settings and achievements
- **Dark Mode**: Toggle light/dark theme
- **Responsive**: Works on all devices

## 🧪 Development

### Backend Testing

```bash
cd backend

# Install dev dependencies
pip install pytest httpx

# Run tests
pytest
```

### Frontend Testing

```bash
cd frontend

# Run linter
npm run lint

# Build for production
npm run build
```

## 📦 Deployment

### Backend (Railway/Render/Heroku)

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn main:app --host 0.0.0.0 --port ${PORT}
```

### Frontend (Vercel/Netlify)

```bash
# Build command
npm run build

# Environment variables
NEXT_PUBLIC_API_URL=https://your-backend-url.com/api/v1
```

### Database (MongoDB Atlas)

1. Create cluster at mongodb.com/atlas
2. Get connection string
3. Update `MONGODB_URL` in backend `.env`

## 🛠️ Technologies Used

### Backend
- FastAPI
- Motor (async MongoDB driver)
- PyMongo
- python-jose (JWT)
- passlib (password hashing)
- Pydantic V2 (validation)

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios (API calls)

## 📝 Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=vocabko
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🐛 Common Issues

### Backend won't start
- Check MongoDB is running: `mongod`
- Verify Python version: `python --version` (need 3.10+)
- Check virtual environment is activated

### Frontend can't connect to API
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend `config.py`

### Authentication errors
- Clear browser localStorage
- Check JWT token hasn't expired
- Verify `SECRET_KEY` matches between requests

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 👨‍💻 Development Team

Built with ❤️ for Korean language learners

## 📄 License

MIT License

---

**Start learning Korean today! 화이팅! 🇰🇷**
