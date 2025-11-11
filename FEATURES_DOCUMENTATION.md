# VocabKo - Advanced Features Documentation

## Overview

VocabKo is a comprehensive Korean vocabulary learning platform with advanced features including spaced repetition, gamification, social learning, and detailed analytics.

## Technology Stack

### Backend (Python FastAPI)
- FastAPI framework for high-performance async API
- MongoDB with Motor (async driver)
- JWT authentication
- Pydantic V2 for data validation
- Swagger UI auto-generated documentation

### Frontend (Next.js 14)
- React 18 with TypeScript
- Tailwind CSS for styling
- Axios for HTTP requests
- App Router architecture

## Advanced Features Implemented

### 1. Spaced Repetition System (SRS)

**Implementation:** SM-2 algorithm for optimal learning intervals

**Endpoints:**
- `GET /api/v1/srs/due` - Get count of due cards
- `GET /api/v1/srs/review` - Get cards for review
- `POST /api/v1/srs/review` - Submit review and update SRS
- `GET /api/v1/srs/stats` - Get SRS statistics

**Features:**
- Automatic interval calculation based on performance
- Quality ratings (0-5) for each review
- Easiness factor adjustment
- Tracks repetitions, intervals, and review history
- Categorizes cards as new, young, or mature

### 2. Leaderboard System

**Endpoints:**
- `GET /api/v1/leaderboard/global` - Global rankings with timeframe filtering
- `GET /api/v1/leaderboard/weekly` - Weekly rankings
- `GET /api/v1/leaderboard/friends` - Friends-only leaderboard
- `GET /api/v1/leaderboard/my-rank` - User's current rank and percentile
- `GET /api/v1/leaderboard/top-learners` - Top learners by category
- `POST /api/v1/leaderboard/points/add` - Add points to user

**Features:**
- Multiple timeframes (all-time, weekly, monthly)
- Points breakdown by category (flashcards, quizzes, streaks)
- Friends comparison
- Percentile ranking
- Top learners by specific metrics

### 3. Daily Challenges

**Endpoints:**
- `GET /api/v1/challenges/daily` - Get today's challenges
- `GET /api/v1/challenges/progress` - Get challenge progress
- `POST /api/v1/challenges/progress/update` - Update challenge progress
- `GET /api/v1/challenges/streak` - Get study streak
- `POST /api/v1/challenges/streak/update` - Update study streak

**Challenge Types:**
- Learn new words
- Review flashcards
- Complete quizzes
- Maintain study streak
- Perfect quiz scores
- Study time goals

**Features:**
- 3 random challenges generated daily
- Progress tracking with completion status
- Points rewards upon completion
- Streak tracking with milestone bonuses
- Automatic progress updates

### 4. Study Sessions Tracking

**Endpoints:**
- `POST /api/v1/sessions/start` - Start study session
- `POST /api/v1/sessions/end/{session_id}` - End session
- `POST /api/v1/sessions/update/{session_id}` - Update session activity
- `GET /api/v1/sessions/active` - Get active session
- `GET /api/v1/sessions/history` - Get session history
- `GET /api/v1/sessions/stats` - Get session statistics

**Tracked Metrics:**
- Duration (minutes)
- Flashcards reviewed
- Quizzes completed
- Words learned
- Accuracy rate
- Points earned

### 5. Vocabulary Categories

**Endpoints:**
- `GET /api/v1/categories` - Get all categories
- `GET /api/v1/categories/{id}` - Get specific category
- `POST /api/v1/categories` - Create category
- `PUT /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Soft delete category
- `GET /api/v1/categories/progress/all` - Get progress in all categories
- `GET /api/v1/categories/stats/{id}` - Get category statistics
- `POST /api/v1/categories/seed` - Seed default categories

**Default Categories:**
- Greetings (인사말)
- Numbers (숫자)
- Food & Dining (음식)
- Family (가족)
- Travel (여행)
- Business (비즈니스)

**Features:**
- Difficulty levels (beginner, intermediate, advanced)
- Progress tracking per category
- Completion percentage
- Custom icons and colors
- Word count tracking

### 6. Advanced Analytics

**Endpoints:**
- `GET /api/v1/analytics/daily` - Daily activity for N days
- `GET /api/v1/analytics/weekly` - Current week statistics
- `GET /api/v1/analytics/monthly` - Monthly statistics
- `GET /api/v1/analytics/heatmap` - Study activity heatmap
- `GET /api/v1/analytics/patterns` - Study patterns analysis
- `GET /api/v1/analytics/performance` - Overall performance metrics

**Analytics Provided:**
- Daily/weekly/monthly breakdowns
- Study time tracking
- Accuracy trends
- Words learned over time
- Study heatmap (GitHub-style)
- Most active hours and days
- Consistency score
- Performance metrics by category

### 7. Gamification System

**Endpoints:**
- `GET /api/v1/gamification/achievements` - Get all achievements
- `GET /api/v1/gamification/achievements/unlocked` - User's achievements
- `GET /api/v1/gamification/achievements/progress` - Progress tracking
- `POST /api/v1/gamification/achievements/check` - Check for unlocks
- `GET /api/v1/gamification/badges` - Get user badges
- `GET /api/v1/gamification/titles` - Get available titles
- `GET /api/v1/gamification/titles/current` - Get current title
- `POST /api/v1/gamification/seed/achievements` - Seed achievements
- `POST /api/v1/gamification/seed/titles` - Seed titles

**Achievement Categories:**
- Learning (words learned milestones)
- Streak (consecutive study days)
- Mastery (words mastered)
- Quiz performance

**Achievement Tiers:**
- Bronze (beginner achievements)
- Silver (intermediate achievements)
- Gold (advanced achievements)
- Platinum (expert achievements)

**Titles System:**
- Beginner (초보자) - 0 points
- Apprentice (견습생) - 500 points
- Scholar (학자) - 2,000 points
- Expert (전문가) - 5,000 points
- Master (마스터) - 10,000 points
- Grandmaster (그랜드마스터) - 20,000 points

### 8. Social Features

**Endpoints:**

**Friends Management:**
- `GET /api/v1/social/friends` - Get friends list
- `POST /api/v1/social/friends/request/{user_id}` - Send friend request
- `GET /api/v1/social/friends/requests/incoming` - Get incoming requests
- `POST /api/v1/social/friends/requests/{id}/accept` - Accept request
- `POST /api/v1/social/friends/requests/{id}/reject` - Reject request
- `DELETE /api/v1/social/friends/{id}` - Remove friend
- `GET /api/v1/social/users/search` - Search users

**Activity Feed:**
- `GET /api/v1/social/feed` - Get activity feed
- `POST /api/v1/social/feed/post` - Create post
- `POST /api/v1/social/feed/post/{id}/like` - Like post
- `POST /api/v1/social/feed/post/{id}/comment` - Comment on post

**Study Groups:**
- `GET /api/v1/social/groups` - Get user's groups
- `POST /api/v1/social/groups` - Create group
- `POST /api/v1/social/groups/{id}/join` - Join group
- `POST /api/v1/social/groups/{id}/leave` - Leave group

**Features:**
- Friend requests system
- User search functionality
- Activity feed from friends
- Post likes and comments
- Study group creation and management
- Social learning features

## Frontend Pages Implemented

### Authentication
- Landing page (`/`) - Marketing homepage
- Login page (`/login`) - User authentication
- Register page (`/register`) - New user registration

### Dashboard
- Main dashboard (`/dashboard`) - Overview with quick stats
- Dashboard layout component - Responsive sidebar navigation

### Features Ready for Implementation
- Flashcards page
- Quiz page
- Progress tracking page
- Leaderboard page
- Challenges page
- Achievements page
- Social feed page
- Profile page

## API Client Library

Complete TypeScript API client (`lib/api.ts`) with:
- Axios instance with interceptors
- JWT token management
- Automatic token refresh
- Error handling
- All endpoint integrations

## Database Collections

### Core Collections
- `users` - User accounts and profiles
- `flashcards` - Korean vocabulary cards
- `srs_cards` - Spaced repetition data

### Features Collections
- `daily_challenges` - Challenge definitions
- `challenge_progress` - User challenge progress
- `study_sessions` - Session tracking
- `study_streaks` - Streak data
- `categories` - Vocabulary categories
- `category_progress` - Category progress
- `achievements` - Achievement definitions
- `user_achievements` - Unlocked achievements
- `badges` - Badge definitions
- `user_badges` - Earned badges
- `titles` - Title/rank definitions
- `friend_requests` - Friend request management
- `posts` - Social feed posts
- `study_groups` - Group definitions

## Running the Application

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Access Swagger documentation at: `http://localhost:8000/docs`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Access frontend at: `http://localhost:3000`

### Environment Variables

**Backend** (`.env`):
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=vocabko
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Testing the Features

### 1. Seed Initial Data
```bash
# Seed flashcards
POST /api/v1/flashcards/seed

# Seed categories
POST /api/v1/categories/seed

# Seed achievements
POST /api/v1/gamification/seed/achievements

# Seed titles
POST /api/v1/gamification/seed/titles
```

### 2. Test User Flow
1. Register a new user
2. Review flashcards to build SRS history
3. Complete daily challenges
4. Take quizzes
5. Check analytics and progress
6. Unlock achievements
7. Connect with friends
8. Join study groups

## Points System

Points are earned through:
- **Flashcard Reviews**: 1 point per card
- **Quiz Completion**: 10-50 points based on score
- **Daily Challenges**: 20-100 points per challenge
- **Study Time**: 1 point per minute (max 60/session)
- **Streak Milestones**: 50 points (weekly), 200 points (monthly)
- **Achievements**: 30-1000 points based on tier

## Future Enhancements

Potential additions:
- Real-time notifications
- Voice recording for pronunciation
- Flashcard creation by users
- Advanced quiz types (writing, listening)
- Mobile app (React Native)
- AI-powered recommendations
- Export/import vocabulary lists
- Premium subscription features

## Support

For issues or questions:
- Check the Swagger documentation at `/docs`
- Review the API client library
- Check MongoDB collections structure

## License

This project is part of the VocabKo Korean learning platform.
