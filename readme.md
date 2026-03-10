# Quiz App

A multi-sport quiz web application built with Flask and PostgreSQL.

## Live Links

- **App**: https://quiz-app-ruby-delta.vercel.app/
- **GitHub**: https://github.com/batcode007/quiz-app

## Database

- **Provider**: Supabase (PostgreSQL)
- **Dashboard**: https://supabase.com/dashboard/project/hnoruwcbngnzvkvnjvyg

## Tech Stack

- **Backend**: Flask 2.3.3 + SQLAlchemy
- **Database**: PostgreSQL (Supabase)
- **Frontend**: HTML/CSS (Tailwind), vanilla JavaScript
- **Deployment**: Vercel

## Local Development

```bash
# Create and activate virtual environment
python -m venv quiz_env
source quiz_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up .env then run:
python app.py
```

App runs at `http://localhost:5000`.

## Environment Variables

```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=admin
MAILGUN_API_KEY=...
MAILGUN_DOMAIN=...
MAIL_DEFAULT_SENDER=...
```
