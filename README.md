# VocabKo - Korean Vocabulary Learning Dashboard

A beautiful, responsive web application for learning Korean vocabulary. VocabKo helps users master new words through interactive vocabulary sets, progress tracking, and an engaging user interface.

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

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FlashCard
```

2. Open the application:
```bash
# Simply open index.html in your browser
open index.html

# Or use a local server (recommended)
python -m http.server 8000
# Then visit http://localhost:8000
```

### No Build Required

This is a standalone HTML application that requires no build process or dependencies. Just open `index.html` in any modern web browser.

## Project Structure

```
FlashCard/
├── index.html          # Main application file
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
