# Dareora

**Dive into the art of daring, where innovative social technology meets thrilling experiences**

Dareora is a dynamic web platform designed for college students to connect through fun challenges and dares. Built with Django and modern web technologies, it creates a safe, competitive, and engaging community environment where students can submit, browse, and complete exciting challenges.

## ✨ Features

### Core Functionality
- **Dare Management**: Submit, browse, and discover community-created challenges
- **Community Wall**: Public showcase of successfully completed dares with verification
- **Interactive Leaderboards**: Recognition system for most active participants
- **Real-time Statistics**: Comprehensive analytics and progress tracking
- **AI-Powered Chat**: Integrated chatbot using Google's Gemini API for user assistance

### User Experience
- **Responsive Design**: Modern, dark-themed UI optimized for all devices
- **Advanced Search & Filtering**: Find dares by category, difficulty, popularity
- **Social Authentication**: Seamless Google OAuth integration
- **Content Moderation**: Admin-reviewed submissions ensure safety and appropriateness
- **Achievement System**: Track completions, likes, and community engagement

### Safety & Moderation
- **Admin Review Process**: All dares reviewed before publication
- **Safety Guidelines**: Built-in safety notes and precautions
- **Content Filtering**: Moderated submissions maintain community standards
- **Verification System**: Proof-based completion tracking

## 🛠️ Technology Stack

### Backend
- **Django 5.2.3** - Web framework
- **PostgreSQL/SQLite** - Database (configurable)
- **Django Allauth** - Authentication & social login
- **Google Generative AI** - Chatbot functionality
- **WhiteNoise** - Static file serving

### Frontend
- **HTML5/CSS3** - Modern semantic markup
- **Vanilla JavaScript** - Interactive features
- **Phosphor Icons** - Icon system
- **Inter Font** - Typography
- **CSS Grid/Flexbox** - Responsive layouts

### Infrastructure
- **Environment Variables** - Secure configuration
- **CSRF Protection** - Security measures
- **Static File Management** - Optimized asset delivery
- **Database Indexing** - Performance optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dareora.git
   cd dareora
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load initial data** (optional)
   ```bash
   python manage.py loaddata initial_categories.json
   python manage.py loaddata initial_difficulties.json
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access the application.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/dareora

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_SECRET_KEY=your-google-secret-key

# AI Chatbot
GEMINI_API_KEY=your-gemini-api-key
```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - Your production domain callback URL

### Gemini AI Setup

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Generate an API key
3. Add to your `.env` file as `GEMINI_API_KEY`

## 📁 Project Structure

```
dareora/
├── daredb/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── dares/                  # Main application
│   ├── models.py          # Data models
│   ├── views.py           # Business logic
│   ├── urls.py            # App-specific URLs
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin interface
│   └── adapters.py        # Social auth adapters
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Landing page
│   ├── dare_list.html     # Dare listings
│   └── ...
├── static/                 # Static assets
├── media/                  # User uploads
├── requirements.txt        # Python dependencies
├── manage.py              # Django management
└── README.md              # This file
```

## 🎨 Design Philosophy

### Visual Identity
- **Dark Theme**: Modern, eye-friendly interface
- **Indigo Accent**: Professional brand color (#4F46E5)
- **Typography**: Inter font for readability
- **Spacing**: Consistent 8px grid system

### User Experience
- **Mobile-First**: Responsive design principles
- **Accessibility**: Semantic HTML and ARIA labels
- **Performance**: Optimized assets and database queries
- **Security**: CSRF protection and input validation

## 🔒 Security Features

- **CSRF Protection**: Built-in Django security
- **Input Validation**: Form and model-level validation
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **Secure Headers**: Security middleware
- **Environment Variables**: Sensitive data protection

## 📊 Database Schema

### Core Models
- **Dare**: Challenge submissions with metadata
- **Category**: Dare categorization (Extreme, Creative, Social, Adventure)
- **DifficultyLevel**: Challenge difficulty ratings
- **DareCompletion**: User completion records
- **DareLike**: User engagement tracking
- **SiteConfiguration**: Admin-configurable settings

### Relationships
- Dare → Category (Many-to-One)
- Dare → DifficultyLevel (Many-to-One)
- Dare → DareCompletion (One-to-Many)
- Dare → DareLike (One-to-Many)


## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

## 📝 API Documentation

### Endpoints
- `GET /api/stats/` - Site statistics JSON
- `POST /chatbot-response/` - AI chatbot interaction
- `GET /search-suggestions/` - Search autocomplete

### Response Formats
```json
{
  "totals": {
    "dares": 150,
    "completions": 89,
    "likes": 234
  },
  "categories": [...],
  "difficulties": [...]
}
```



## 🙏 Acknowledgments

- **Django Community** - Framework and documentation
- **Google** - OAuth and Gemini AI services
- **Phosphor Icons** - Beautiful icon system
- **Inter Font** - Typography design

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ajitashwath/dare-exchange/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ajitashwath/dare-exchange/discussions)

---

**Built with ❤️ for the college community**

*Dareora - Where innovation meets adventure*
