from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    quizzes = db.relationship('Quiz', backref='user', lazy=True)
    
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
                'average_score': 0,
                'best_score': 0,
                'total_time': 0,
                'favorite_category': 'None'
            }
        
        total_score = sum(quiz.score for quiz in self.quizzes)
        total_time = sum(quiz.time_taken or 0 for quiz in self.quizzes)
        best_score = max(quiz.score for quiz in self.quizzes) if self.quizzes else 0
        
        category_count = {}
        for quiz in self.quizzes:
            cat_name = quiz.category.name
            category_count[cat_name] = category_count.get(cat_name, 0) + 1
        
        favorite_category = max(category_count.items(), key=lambda x: x[1])[0] if category_count else 'None'
        
        return {
            'total_quizzes': total_quizzes,
            'average_score': round(total_score / total_quizzes, 1) if total_quizzes > 0 else 0,
            'best_score': best_score,
            'total_time': total_time,
            'favorite_category': favorite_category
        }

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    categories = db.relationship('Category', backref='sport', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('Question', backref='category', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # mcq, true_false, fill_blank
    difficulty = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    options = db.Column(db.Text)  # JSON string for MCQ options
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_options(self):
        if self.options:
            return json.loads(self.options)
        return []
    
    def set_options(self, options_list):
        self.options = json.dumps(options_list)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=10)
    time_taken = db.Column(db.Integer)  # in seconds
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', backref='quizzes')
    answers = db.relationship('QuizAnswer', backref='quiz', lazy=True)

class QuizAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_answer = db.Column(db.String(500))
    is_correct = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer)  # in seconds
    
    question = db.relationship('Question', backref='quiz_answers')