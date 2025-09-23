# 🏏 Quiz App

A comprehensive web-based quiz application built with Flask and PostgreSQL, featuring multiple question types, difficulty levels, real-time scoring, and an admin panel for content management.

![Quiz App](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Admin Panel](#admin-panel)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🎯 Core Quiz Features
- **10 Questions per Quiz**: Structured quiz sessions with exactly 10 questions
- **Multiple Question Types**: 
  - Multiple Choice Questions (MCQ)
  - True/False questions
  - Fill in the blanks
- **Timer System**: 60-second countdown per question with visual progress
- **Difficulty Levels**: Easy, Medium, and Hard questions
- **Categories**: 
  - World Cup
  - Batting Specific
  - Bowling Specific
  - Fielding
  - Cricket History
  - Rules & Regulations
- **Real-time Scoring**: Instant feedback and score calculation
- **Detailed Results**: Complete quiz review with explanations

### 🎨 User Experience
- **Mobile-Responsive**: Optimized for all device sizes
- **Modern UI**: Clean, intuitive interface with Tailwind CSS
- **Progress Tracking**: Visual indicators for quiz progression
- **Interactive Elements**: Smooth animations and transitions
- **Accessibility**: Keyboard navigation and screen reader support

### ⚙️ Admin Features
- **Content Management**: Add, edit, and manage questions
- **Category Management**: Organize questions by cricket topics
- **Analytics Dashboard**: View quiz statistics and performance
- **Question Types Support**: Easy creation of all question formats
- **Bulk Operations**: Efficient content management tools

## 🏗️ Architecture

The application follows a layered architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│             Frontend Layer              │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │   HTML/CSS  │  │   JavaScript    │   │
│  │ (Tailwind)  │  │   (Vanilla JS)  │   │
│  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────┐
│          Application Layer              │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │    Flask    │  │     Routes      │   │
│  │   Server    │  │   & Business    │   │
│  │             │  │     Logic       │   │
│  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────┐
│            Data Layer                   │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │ SQLAlchemy  │  │   PostgreSQL    │   │
│  │    ORM      │  │    Database     │   │
│  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────┘
```

See the [Architecture Diagram](#architecture-diagram) section for a detailed visual representation.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/cricket-quiz-app.git
cd cricket-quiz-app
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv cricket_quiz_env

# Activate virtual environment
# On Linux/macOS:
source cricket_quiz_env/bin/activate

# On Windows:
cricket_quiz_env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

```sql
-- Connect to PostgreSQL as superuser and run:
CREATE DATABASE cricket_quiz;
CREATE USER quiz_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE cricket_quiz TO quiz_user;
```

### Step 5: Configure Environment

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://quiz_user:your_secure_password@localhost/cricket_quiz
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_admin_password_change_this
FLASK_ENV=development
```

### Step 6: Initialize Database

```bash
python init_db.py
```

### Step 7: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for session management | `cricket-quiz-secret-key-2024` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://username:password@localhost/cricket_quiz` |
| `ADMIN_USERNAME` | Admin panel username | `admin` |
| `ADMIN_PASSWORD` | Admin panel password | `admin123` |
| `FLASK_ENV` | Flask environment mode | `production` |

### Database Configuration

The application uses PostgreSQL as the primary database. Ensure your database server is running and accessible with the credentials specified in your `.env` file.

## 📖 Usage

### For Quiz Takers

1. **Start Quiz**: Visit the homepage and fill out the quiz form
   - Enter your name
   - Select a category (World Cup, Batting, Bowling, etc.)
   - Choose difficulty level (Easy, Medium, Hard)

2. **Take Quiz**: 
   - Answer 10 questions with 60 seconds per question
   - Questions can be MCQ, True/False, or Fill-in-the-blank
   - Immediate feedback after each answer

3. **View Results**:
   - See your final score and performance metrics
   - Review detailed explanations for each question
   - Compare your performance across categories

### For Administrators

1. **Access Admin Panel**: Navigate to `/admin`
   - Default credentials: `admin` / `admin123`

2. **Manage Content**:
   - Add new questions with explanations
   - Organize questions by category and difficulty
   - View quiz statistics and user performance

## 🔌 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Homepage with quiz categories |
| `POST` | `/start_quiz` | Initialize a new quiz session |
| `GET` | `/quiz` | Quiz interface page |
| `GET` | `/get_question/<int:question_num>` | Fetch specific question |
| `POST` | `/submit_answer` | Submit answer for current question |
| `POST` | `/finish_quiz` | Complete quiz and save results |
| `GET` | `/results/<int:quiz_id>` | Display quiz results |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin` | Admin login page |
| `POST` | `/admin/login` | Authenticate admin user |
| `GET` | `/admin/dashboard` | Admin dashboard with statistics |
| `GET` | `/admin/add_question` | Add new question form |
| `POST` | `/admin/save_question` | Save new question to database |
| `GET` | `/admin/logout` | Logout admin user |

### Request/Response Examples

#### Start Quiz

**Request:**
```json
POST /start_quiz
{
  "user_name": "John Doe",
  "category_id": 1,
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "quiz_id": 123,
  "redirect": "/quiz"
}
```

#### Submit Answer

**Request:**
```json
POST /submit_answer
{
  "question_id": 45,
  "answer": "England",
  "time_taken": 23
}
```

**Response:**
```json
{
  "correct": true,
  "correct_answer": "England",
  "explanation": "England won their first Cricket World Cup in 2019 defeating New Zealand in the final."
}
```

## 🗄️ Database Schema

### Tables Overview

```sql
-- Categories table
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table
CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    question_type VARCHAR(20) NOT NULL, -- 'mcq', 'true_false', 'fill_blank'
    difficulty VARCHAR(20) NOT NULL,    -- 'easy', 'medium', 'hard'
    options TEXT,                       -- JSON string for MCQ options
    correct_answer VARCHAR(500) NOT NULL,
    explanation TEXT,
    category_id INTEGER REFERENCES category(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quizzes table
CREATE TABLE quiz (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    category_id INTEGER REFERENCES category(id),
    difficulty VARCHAR(20) NOT NULL,
    score INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 10,
    time_taken INTEGER,                 -- in seconds
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quiz answers table
CREATE TABLE quiz_answer (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quiz(id),
    question_id INTEGER REFERENCES question(id),
    user_answer VARCHAR(500),
    is_correct BOOLEAN DEFAULT FALSE,
    time_taken INTEGER                  -- in seconds
);
```

### Relationships

- **Category → Question**: One-to-Many (One category can have multiple questions)
- **Category → Quiz**: One-to-Many (One category can be used in multiple quizzes)
- **Quiz → QuizAnswer**: One-to-Many (One quiz contains multiple answers)
- **Question → QuizAnswer**: One-to-Many (One question can be answered in multiple quizzes)

## 👑 Admin Panel

### Features

- **Dashboard**: Overview of system statistics
- **Question Management**: Add, edit, and organize questions
- **Category Management**: Create and manage quiz categories
- **Analytics**: View quiz performance and user statistics

### Default Credentials

For development/testing purposes:
- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Security Note**: Change these credentials before deploying to production!

### Adding Questions

1. Navigate to Admin Dashboard → Add Question
2. Fill in question details:
   - Question text
   - Question type (MCQ/True-False/Fill-in-blank)
   - Category and difficulty level
   - Correct answer and explanation
3. For MCQ questions, provide 2-4 answer options
4. Save the question

## 🛠️ Development

### Project Structure

```
cricket_quiz/
├── app.py                 # Main Flask application
├── models.py              # Database models (SQLAlchemy)
├── config.py              # Configuration settings
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md              # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── app.js         # Frontend JavaScript
│
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Homepage
    ├── quiz.html          # Quiz interface
    ├── results.html       # Results page
    └── admin/
        ├── login.html     # Admin login
        ├── dashboard.html # Admin dashboard
        └── add_question.html # Add question form
```

### Running in Development Mode

```bash
# Set environment variable
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows

# Run with debug mode
python app.py
```

### Adding New Features

The application is designed to be easily extensible:

1. **New Question Types**: Add to `models.py` and update frontend logic
2. **New Categories**: Use admin panel or add via database
3. **New Difficulty Levels**: Update models and form options
4. **Analytics Features**: Extend admin dashboard with new queries

## 🧪 Testing

### Manual Testing Checklist

- [ ] User can start a quiz with different categories/difficulties
- [ ] Timer functions correctly (60 seconds per question)
- [ ] All question types work (MCQ, True/False, Fill-in-blank)
- [ ] Scoring is accurate
- [ ] Results page shows detailed information
- [ ] Admin panel allows adding questions
- [ ] Mobile responsiveness works
- [ ] Database operations complete successfully

### Sample Test Data

The `init_db.py` script includes sample questions for testing. Additional test data can be added through the admin panel.

## 🚀 Deployment

### Production Checklist

- [ ] Change default admin credentials
- [ ] Set strong `SECRET_KEY`
- [ ] Configure production PostgreSQL database
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS
- [ ] Configure proper logging
- [ ] Set up database backups
- [ ] Configure monitoring

### Environment-Specific Settings

Create different configuration files for different environments:

```python
# config.py
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Production-specific settings
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes

### Reporting Issues

Please use the GitHub issue tracker to report bugs or request features. Include:

- Detailed description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment information (OS, Python version, etc.)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database system
- **Tailwind CSS** - Styling framework
- **Cricket Community** - Inspiration and question content

## 📞 Support

If you have questions or need help:

1. Check the [documentation](#table-of-contents)
2. Search [existing issues](../../issues)
3. Create a [new issue](../../issues/new) if needed

---

**Happy Quizzing! 🏏**

Made with ❤️ for cricket enthusiasts worldwide.