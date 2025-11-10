# VocabKo Backend - NestJS API

Complete backend implementation for the VocabKo Korean Vocabulary Learning Platform.

## 🚀 Technology Stack

- **Framework**: NestJS 10.x
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: class-validator & class-transformer
- **Language**: TypeScript

## 📁 Project Structure

```
FlashCard/
├── src/
│   ├── auth/                 # Authentication module
│   │   ├── dto/             # Data Transfer Objects
│   │   ├── guards/          # Auth guards
│   │   ├── strategies/      # Passport strategies
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── auth.module.ts
│   ├── users/               # User management
│   │   ├── schemas/         # Mongoose schemas
│   │   ├── dto/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   └── users.module.ts
│   ├── flashcards/          # Flashcard management
│   │   ├── schemas/
│   │   ├── dto/
│   │   ├── flashcards.controller.ts
│   │   ├── flashcards.service.ts
│   │   └── flashcards.module.ts
│   ├── quiz/                # Quiz functionality
│   │   ├── schemas/
│   │   ├── dto/
│   │   ├── quiz.controller.ts
│   │   ├── quiz.service.ts
│   │   └── quiz.module.ts
│   ├── progress/            # Progress tracking
│   │   ├── schemas/
│   │   ├── dto/
│   │   ├── progress.controller.ts
│   │   ├── progress.service.ts
│   │   └── progress.module.ts
│   ├── app.module.ts        # Root module
│   └── main.ts              # Application entry point
├── index.html               # Frontend dashboard
├── flashcard.html           # Flashcard interface
├── quiz.html                # Quiz interface
├── progress.html            # Progress tracking
├── profile.html             # User profile
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
├── nest-cli.json            # NestJS CLI config
└── .env                     # Environment variables
```

## 🔧 Installation & Setup

### Prerequisites

- Node.js >= 18.x
- npm or yarn
- MongoDB (local or MongoDB Atlas)

### Step 1: Install Dependencies

```bash
npm install
```

### Step 2: Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Application
PORT=3000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/vocabko

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=7d

# Frontend
FRONTEND_URL=http://localhost:3000
```

### Step 3: Start MongoDB

**Option A: Local MongoDB**
```bash
# Start MongoDB service
mongod