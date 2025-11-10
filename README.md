# VocabKo - Korean Vocabulary Learning Platform

A complete full-stack web application for learning Korean vocabulary. VocabKo features a **NestJS backend** with MongoDB database and an interactive frontend with flashcards, quizzes, progress tracking, and user profiles.

## 🎯 Full-Stack Architecture

### Backend
- **Framework**: NestJS 10.x with TypeScript
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: JWT-based auth with Passport
- **API**: RESTful API with validation

### Frontend
- **HTML5, CSS3, JavaScript**
- **Tailwind CSS** for styling
- **Responsive** design for all devices
- **Dark mode** support

## Features

### 🎨 Modern Design
- Clean, intuitive interface built with Tailwind CSS
- Responsive design that works on all devices (mobile, tablet, desktop)
- Dark mode support with smooth transitions
- Custom color scheme optimized for learning

### 📚 Vocabulary Sets
- **Recently Studied Sets**: Quick access to your ongoing learning materials
- **Featured Sets**: Curated vocabulary collections covering various topics
- Progress bars to track your learning journey
- Beautiful card-based layout with hover effects

### 📊 Progress Tracking
- Weekly progress visualization with bar charts
- Streak counter to maintain motivation
- Real-time statistics on words learned

### 🌓 Dark Mode
- Toggle between light and dark themes
- Automatic theme persistence using localStorage
- Eye-friendly color schemes for extended study sessions

## Technology Stack

- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first CSS framework
- **Google Fonts**: Lexend font family for optimal readability
- **Material Symbols**: Icon system for UI elements
- **Vanilla JavaScript**: Interactive features without dependencies

## Getting Started

### Backend Setup

1. **Install Dependencies**
```bash
npm install
```

2. **Configure Environment**
Create a `.env` file (see `.env.example`):
```env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/vocabko
JWT_SECRET=your-secret-key
```

3. **Start MongoDB**
```bash
# Local MongoDB
mongod

# Or use MongoDB Atlas (cloud)
```

4. **Run the Backend**
```bash
# Development mode
npm run start:dev

# Production mode
npm run build
npm run start:prod
```

The backend will run on `http://localhost:3000`

### Frontend Access

Once the backend is running, access the application:
- Main Dashboard: `http://localhost:3000/index.html`
- Flashcards: `http://localhost:3000/flashcard.html`
- Quiz: `http://localhost:3000/quiz.html`
- Progress: `http://localhost:3000/progress.html`
- Profile: `http://localhost:3000/profile.html`

### API Endpoints

All API endpoints are prefixed with `/api`:
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/users/profile` - Get user profile
- `GET /api/flashcards` - Get all flashcards
- `GET /api/quiz/questions` - Get quiz questions
- `POST /api/quiz/submit` - Submit quiz answers
- `GET /api/progress` - Get user progress

## Project Structure

```
FlashCard/
├── index.html          # Main dashboard page
├── flashcard.html      # Interactive flashcard learning interface
├── quiz.html           # Interactive quiz with multiple-choice questions
├── progress.html       # Progress tracking and statistics
├── profile.html        # User profile and achievements
└── README.md          # Project documentation
```

## Features in Detail

### Navigation Bar
- Logo and branding
- Quick links to All Sets, Practice, and Profile
- Search functionality for finding vocabulary sets
- Notification center
- User profile access
- Dark mode toggle

### Hero Section
- Eye-catching Korean-themed imagery
- Clear call-to-action
- Motivational messaging

### Vocabulary Cards
- Visual thumbnails for each set
- Word count display
- Progress indicators
- Hover effects for better interactivity

### Progress Dashboard
- 7-day activity visualization
- Daily learning statistics
- Streak tracking with fire icon
- Encouraging messages

### Flashcard Learning Interface
- **Interactive 3D Flip Cards**: Smooth card flipping animation to reveal translations
- **50 Korean Vocabulary Words**: Comprehensive word database with examples
- **Navigation Controls**: Previous, Flip, and Next buttons for easy navigation
- **Progress Tracking**: Visual progress bar showing completion status
- **Smart Learning**: Mark cards as "I know this" or "Review later"
- **Audio Pronunciation**: Text-to-speech for Korean words (Web Speech API)
- **Keyboard Shortcuts**:
  - Arrow Left/Right: Navigate between cards
  - Space/Enter: Flip card
  - Key 1: Mark as "I know this"
  - Key 2: Mark as "Review later"
- **Auto-advance**: Automatically moves to next card after marking progress

### Interactive Quiz
- **20 Multiple-Choice Questions**: Test your Korean vocabulary knowledge
- **Instant Feedback**: Get immediate feedback on your answers
- **Progress Tracking**: Visual progress bar showing quiz completion
- **Score Summary**: View detailed results with correct/incorrect counts
- **Audio Pronunciation**: Hear Korean words pronounced correctly
- **Try Again**: Restart the quiz to improve your score
- **Randomized Options**: Answer choices are shuffled for better learning

### Progress Tracking Dashboard
- **Learning Statistics**: Track words learned, daily streak, and overall accuracy
- **Visual Charts**: View your learning pace over the last 30 days
- **Monthly Activity Calendar**: See your study activity at a glance
- **Achievement Tracking**: Monitor your progress towards learning goals
- **Performance Metrics**: 92% accuracy rate with detailed breakdowns
- **Motivation Tools**: Keep track of streaks and milestones

### User Profile
- **Personal Information**: Manage username, email, and password
- **Profile Picture**: Upload and customize your avatar
- **Learning Goals**: Set daily word learning targets (10-50 words/day)
- **Progress Overview**: View total words learned and study streak
- **Achievement Badges**: Earn and display badges for milestones:
  - 7-Day Streak
  - First 50 Words
  - Grammar Guru
  - Perfect Score
  - Top Learner
  - 30-Day Streak
- **Daily Goal Progress**: Visual progress bar for daily targets

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## Customization

### Colors
The application uses custom color variables defined in the Tailwind config:
- Primary: `#2b6cee` (Blue)
- Background Light: `#f6f6f8`
- Background Dark: `#101622`
- Coral: `#ff9b85` (Accent color for streaks)

### Adding New Vocabulary Sets

To add new vocabulary sets, duplicate the card structure in the HTML:

```html
<div class="flex h-full flex-1 flex-col gap-4 rounded-lg min-w-60 vocab-card">
    <div class="w-full bg-center bg-no-repeat aspect-video bg-cover rounded-lg flex flex-col cursor-pointer"
         style='background-image: url("YOUR_IMAGE_URL");'></div>
    <div>
        <p class="text-gray-900 dark:text-gray-100 text-base font-medium leading-normal">Set Name</p>
        <p class="text-gray-500 dark:text-gray-400 text-sm font-normal leading-normal">X words</p>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-2">
            <div class="bg-primary h-1.5 rounded-full progress-bar" style="width: Y%"></div>
        </div>
    </div>
</div>
```

## Future Enhancements

- [ ] Backend integration for user data persistence
- [ ] Interactive flashcard study mode
- [ ] Spaced repetition algorithm
- [ ] Audio pronunciation guides
- [ ] Quiz and testing features
- [ ] Social features (share progress, compete with friends)
- [ ] Mobile app versions
- [ ] Additional language support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Tailwind CSS for the excellent utility-first framework
- Google Fonts for the Lexend font family
- Material Symbols for the icon system
- Image sources from Google's AIDA public library

---

**Happy Learning! 화이팅! (Fighting!)** 🇰🇷
