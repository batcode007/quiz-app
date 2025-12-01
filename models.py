from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Define db globally (single instance for the entire app)
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    quizzes = db.relationship('Quiz', backref='user', lazy=True)

    @property
    def full_name(self):
        """Return full name from first and last name"""
        return f"{self.first_name} {self.last_name}"
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def get_stats(self):
        total_quizzes = len(self.quizzes)
        if total_quizzes == 0:
            return {
                'total_quizzes': 0,
                'average_score_percentage': 0,
                'best_score': 0,
                'total_time': 0,
                'favorite_category': 'None'
            }
        
        total_score = sum(quiz.score for quiz in self.quizzes)
        total_questions_sum = sum(quiz.total_questions for quiz in self.quizzes)
        total_time = sum(quiz.time_taken or 0 for quiz in self.quizzes)
        best_score = max(quiz.score for quiz in self.quizzes) if self.quizzes else 0
        
        category_count = {}
        for quiz in self.quizzes:
            cat_name = quiz.category.name
            category_count[cat_name] = category_count.get(cat_name, 0) + 1
        
        favorite_category = max(category_count.items(), key=lambda x: x[1])[0] if category_count else 'None'
        average_score_percentage = (total_score / total_questions_sum) * 100 if total_questions_sum > 0 else 0
        
        return {
            'total_quizzes': total_quizzes,
            'average_score_percentage': round(average_score_percentage, 1) if total_quizzes > 0 else 0,
            'best_score': best_score,
            'total_time': total_time,
            'favorite_category': favorite_category
        }
    
    __table_args__ = (
        db.Index('idx_users_created_at', 'created_at'),
        db.Index('idx_users_last_login', 'last_login'),
    )

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)
    categories = db.relationship('Category', backref='sport', lazy=True)
    
    __table_args__ = (
        db.Index('idx_sports_created_at', 'created_at'),
    )

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    question_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('Question', backref='category', lazy=True)
    
    __table_args__ = (
        db.Index('idx_categories_created_at', 'created_at'),
        db.Index('idx_categories_sport_id', 'sport_id'),
    )

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    options = db.Column(db.Text)
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_options(self):
        if self.options:
            return json.loads(self.options)
        return []
    
    def set_options(self, options_list):
        self.options = json.dumps(options_list)
    
    __table_args__ = (
        db.Index('idx_questions_created_at', 'created_at'),
        db.Index('idx_questions_category_id', 'category_id'),
    )

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship('Category', backref='quizzes')
    answers = db.relationship('QuizAnswer', backref='quiz', lazy=True)
    
    __table_args__ = (
        db.Index('idx_quizzes_completed_at', 'completed_at'),
        db.Index('idx_quizzes_user_id', 'user_id'),
        db.Index('idx_quizzes_category_id', 'category_id'),
    )

class QuizAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_answer = db.Column(db.String(500))
    is_correct = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    question = db.relationship('Question', backref='quiz_answers')
    
    __table_args__ = (
        db.Index('idx_quiz_answers_quiz_id', 'quiz_id'),
        db.Index('idx_quiz_answers_question_id', 'question_id'),
    )

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_settings_key', 'key'),
    )