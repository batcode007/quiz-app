# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-sport quiz web application built with Flask and PostgreSQL. The application features user authentication, multiple question types, difficulty levels, real-time scoring, and an admin panel for content management. It includes a data warehouse component for exporting quiz data to AWS S3 and Redshift.

### Technology Stack

- **Backend**: Flask 2.3.3 with SQLAlchemy ORM
- **Database**: PostgreSQL (production: Supabase)
- **Frontend**: HTML/CSS (Tailwind), vanilla JavaScript
- **Migrations**: Flask-Migrate (Alembic)
- **Data Warehouse**: boto3 for S3, pandas/pyarrow for data processing
- **Deployment**: Gunicorn with Heroku/similar platforms

## Development Commands

### Environment Setup

```bash
# Create virtual environment
python -m venv quiz_env

# Activate environment
source quiz_env/bin/activate  # macOS/Linux
quiz_env\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

### Database Operations

```bash
# Initialize database (creates tables and default settings)
python init_db.py

# Run database migrations
flask db migrate -m "migration message"
flask db upgrade

# Downgrade migration
flask db downgrade
```

### Running the Application

```bash
# Development mode (with debug)
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
python app.py

# Production mode (via Gunicorn)
gunicorn app:create_app
```

The application runs on `http://localhost:5000` by default.

### Data Warehouse Operations

```bash
# Export raw data to S3
python warehouse/export_raw_data.py

# Create Redshift tables
python warehouse/create_redshift_tables.py

# Load data to Redshift
python warehouse/load_to_redshift.py
```

## Architecture

### Application Structure

The application follows a factory pattern with clear separation of concerns:

```
quiz_app/
├── app.py                    # Flask app factory (create_app)
├── models.py                 # SQLAlchemy models (User, Sport, Category, Question, Quiz, etc.)
├── config.py                 # Configuration (SECRET_KEY, DATABASE_URL)
├── init_db.py                # Database initialization script
├── migrations/               # Alembic database migrations
├── templates/
│   ├── base.html            # Base template with common layout
│   ├── index.html           # Homepage (category selection)
│   ├── quiz.html            # Quiz interface
│   ├── quiz_question.html   # Individual question display
│   ├── quiz_result.html     # Quiz results
│   ├── profile.html         # User profile with stats
│   ├── auth/                # Login/Register templates
│   └── admin/               # Admin panel templates
├── static/
│   ├── css/                 # Custom styles
│   ├── js/                  # Frontend JavaScript
│   └── images/              # Static images
├── scripts/                 # Data import/scraping scripts
└── warehouse/               # Data export to S3/Redshift
```

### Database Models

**Core Models:**

- **User**: User accounts with password hashing, login tracking, and statistics
- **Sport**: Top-level category (e.g., Cricket, Football/EPL)
- **Category**: Sub-categories within sports (e.g., "Batting Specific", "EPL History")
- **Question**: Quiz questions with type (mcq/true_false/fill_blank), difficulty, options, correct answer, explanation
- **Quiz**: Quiz session tracking user, category, difficulty, score, time
- **QuizAnswer**: Individual answers within a quiz session
- **Settings**: App-wide settings (e.g., default quiz length)

**Relationships:**
- Sport → Categories (one-to-many)
- Category → Questions (one-to-many)
- User → Quizzes (one-to-many)
- Quiz → QuizAnswers (one-to-many)
- Question → QuizAnswers (one-to-many, across multiple quizzes)

**Indexes:** Models include database indexes on frequently queried columns (user_id, category_id, created_at, etc.) for performance optimization.

### Session Management

The application uses Flask sessions for:
- **Authentication**: `session['user_id']`, `session['username']`, `session['full_name']`
- **Admin**: `session['admin']` (boolean flag)
- **Quiz State**: `session['quiz_id']`, `session['questions']` (list of question IDs), `session['current_question']`, `session['score']`, `session['answers']`, `session['start_time']`

Sessions expire after 30 minutes (`PERMANENT_SESSION_LIFETIME` in config.py).

### Application Factory Pattern

The app uses a factory pattern in `app.py`:
- `create_app(host=None, port=None)` initializes Flask app, SQLAlchemy, Flask-Migrate
- All routes are registered inside `create_app()` within an application context
- This pattern supports testing and avoids circular imports
- Models must import `db` from `models.py` (single SQLAlchemy instance)

### Quiz Flow

1. **User logs in** → redirected to index page showing sports and categories
2. **Start Quiz** → POST to `/start_quiz` with `category_id` and `difficulty`
   - Fetches random sample of questions matching criteria
   - Creates Quiz record in database
   - Stores question IDs in session
3. **Answer Questions** → GET/POST to `/quiz/<question_num>`
   - POST submits answer, saves to QuizAnswer table
   - Redirects to next question or submits quiz
4. **Submit Quiz** → POST to `/submit_quiz`
   - Updates Quiz record with final score and time
   - Clears quiz session data
5. **View Results** → GET `/results/<quiz_id>`
   - Shows score, time, detailed question review with explanations

### Admin Panel

- **Access**: `/admin` (separate login from user accounts)
- **Authentication**: Username/password from environment variables (not database)
- **Features**:
  - Dashboard with system statistics
  - Add questions (POST to `/admin/save_question`)
  - Manage settings (quiz length)
  - View categories and question counts

**Security Note**: Admin credentials stored in `.env` file, not hashed by default. Change `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH` before production.

## Configuration

### Environment Variables (.env)

Required variables:

```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=admin
S3_BUCKET=warehouse-dev  # For data export features
```

**Database URL Format**:
- Local: `postgresql://username:password@localhost/quiz_app`
- Supabase: `postgresql://postgres:password@db.xxx.supabase.co:5432/postgres`

The application uses `python-dotenv` to load environment variables from `.env` file.

## Key Development Patterns

### Password Hashing

User passwords are hashed with `werkzeug.security`:
```python
user.set_password(password)  # Hashes with pbkdf2:sha256
user.check_password(password)  # Verifies hash
```

### Question Options Handling

MCQ question options are stored as JSON strings in the database:
```python
question.set_options(['Option 1', 'Option 2', 'Option 3'])  # Stores as JSON
options = question.get_options()  # Returns list
```

### User Statistics

The `User` model has a `get_stats()` method that calculates:
- Total quizzes taken
- Average score percentage
- Best score
- Total time spent
- Favorite category

This is used in the profile page (`/profile`).

### Database Queries with Filters

Common query patterns:
```python
# Active categories (with questions)
Category.query.filter(Category.question_count > 0).all()

# Questions by category and difficulty
Question.query.filter_by(category_id=cat_id, difficulty=difficulty).all()

# User's quiz history (paginated)
Quiz.query.filter_by(user_id=user_id).order_by(Quiz.completed_at.desc()).paginate(page=page, per_page=5)
```

### Session-based Quiz State

Quiz state is stored in Flask session (not database) during active quiz:
- This allows abandoning quizzes without database cleanup
- Quiz record is created at start, updated at completion
- Individual answers are saved immediately after each question

## Data Scripts

### scripts/db_insert.py

Bulk inserts questions into the database. Used for importing scraped quiz data (e.g., from Sporcle). Configure `DB_CONFIG` with local database credentials and set `SPORT_ID` and `CATEGORY_ID` constants.

### scripts/sporcle_*.py

Web scrapers for extracting quiz questions from external sources. These scripts parse HTML and extract questions, options, and answers.

### warehouse/export_raw_data.py

Exports all database tables to S3 as Parquet files for data warehousing. Requires AWS credentials and S3_BUCKET environment variable.

### warehouse/create_redshift_tables.py & load_to_redshift.py

Creates Redshift tables and loads data from S3 Parquet files for analytics.

## Deployment

### Vercel Deployment

**Important**: Vercel is designed for serverless functions. This Flask application requires modifications to work properly on Vercel.

#### Required Files

1. **vercel.json** (create in project root):
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

2. **Modified requirements.txt** (for Vercel compatibility):
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.9
python-dotenv==1.0.0
Flask-WTF==1.2.1
pyarrow
boto3
flask_migrate
```

**Note**: Use `psycopg2-binary==2.9.9` (newer version) to avoid pg_config errors on Vercel.

3. **Create api/index.py** (Vercel serverless entry point):
```python
from app import create_app

app = create_app()
```

#### Environment Variables in Vercel

Configure these in Vercel dashboard (Settings → Environment Variables):
- `DATABASE_URL`: Your PostgreSQL connection string
- `SECRET_KEY`: Strong random key
- `ADMIN_USERNAME`: Admin username
- `ADMIN_PASSWORD_HASH`: Admin password
- `FLASK_ENV`: production

#### Known Limitations with Vercel

- **Serverless architecture**: Each request creates a new function instance
- **Cold starts**: First request may be slow
- **Session storage**: Flask sessions work but may have issues with multiple instances
- **Database connections**: Connection pooling is limited
- **File uploads**: Use S3 or similar, not local filesystem
- **Background jobs**: Not supported (use external task queue)

**Recommendation**: Consider using Heroku, Railway, or Render for traditional Flask apps with persistent connections.

### Heroku/Railway/Render Deployment

The `Procfile` defines the web process:
```
web: gunicorn app:create_app
```

**Important**: Gunicorn expects the factory function, not an app instance.

These platforms are better suited for Flask applications with SQLAlchemy and persistent database connections.

### Production Checklist

1. Set strong `SECRET_KEY` in environment
2. Change `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH`
3. Set `FLASK_ENV=production`
4. Configure production PostgreSQL database (e.g., Supabase)
5. Run database migrations: `flask db upgrade`
6. Ensure `.env` file is not committed (already in `.gitignore`)
7. Configure session security (HTTPS, secure cookies)
8. Set up database connection pooling for production
9. Configure logging to stdout for platform log aggregation

## Common Issues

### Circular Import Error

If you encounter circular import errors:
- Ensure `db` is imported from `models.py`, not created in `app.py`
- Import models inside `create_app()` after `db.init_app(app)`
- Use `with app.app_context():` when needed

### Migration Conflicts

If migrations fail:
```bash
# Check current migration state
flask db current

# Stamp the database with a specific revision
flask db stamp head

# Generate new migration
flask db migrate
```

### Session Data Persistence

Quiz session data is cleared on logout or quiz submission. If session data seems stale, check:
- Session cookie expiration (30 minutes)
- Proper session clearing in logout/finish_quiz routes

## Testing

### Manual Testing Workflow

1. Register a new user at `/register`
2. Log in at `/login`
3. Select a category and difficulty at `/`
4. Take a quiz (answer questions)
5. Review results at `/results/<quiz_id>`
6. Check profile at `/profile` for statistics
7. Test admin panel at `/admin`

### Database Testing

For development, use a separate test database:
```bash
# Create test database
createdb quiz_app_test

# Set test DATABASE_URL
export DATABASE_URL=postgresql://user:pass@localhost/quiz_app_test

# Initialize test database
python init_db.py
```

## Git Workflow

Current branch: `development` (check git status for active branch)

Files to ignore (already in `.gitignore`):
- `.env` (sensitive credentials)
- `quiz_env/` (virtual environment)
- `__pycache__/`, `*.pyc` (Python cache)
- `app.log` (application logs)

## Logging

Application logs are written to `app.log` with format:
```
%(asctime)s - %(levelname)s - %(message)s
```

For debugging, check `app.log` for errors and warnings during development.
