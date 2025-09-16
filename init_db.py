from app import create_app
from models import User, Sport, Category, Question, Settings

def init_db():
    # Create the Flask app instance and get the initialized db
    app = create_app()
    from models import db  # Import db after create_app to ensure it's the initialized instance
    
    # Ensure the app context is used for database operations
    with app.app_context():
        # Create tables only if they don't exist
        db.create_all()
        
        # Check if Settings table has the default quiz length; add if missing
        if not Settings.query.filter_by(key='default_quiz_length').first():
            default_quiz_length = Settings(
                key='default_quiz_length',
                value='10',
                description='Default number of questions per quiz'
            )
            db.session.add(default_quiz_length)
            db.session.commit()
            print("Added default quiz length setting.")
        else:
            print("Default quiz length setting already exists.")
        
        print("Database setup completed. Existing data preserved.")

if __name__ == '__main__':
    init_db()