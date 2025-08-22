from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from models import db, Category, Question, Quiz, QuizAnswer, User, Sport
from config import Config
import random
import json
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
@login_required
def index():
    sports = Sport.query.all()
    categories = Category.query.all()
    user = User.query.get(session['user_id'])
    user_stats = user.get_stats()
    recent_quizzes = Quiz.query.filter_by(user_id=user.id).order_by(Quiz.completed_at.desc()).limit(5).all()
    return render_template('index.html', sports=sports, categories=categories, user=user, user_stats=user_stats, recent_quizzes=recent_quizzes)

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data['full_name']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            user.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('index')})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    user_stats = user.get_stats()
    
    # Get quiz history with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    quiz_history = Quiz.query.filter_by(user_id=user.id)\
                            .order_by(Quiz.completed_at.desc())\
                            .paginate(page=page, per_page=per_page, error_out=False)
    
    # Get category-wise performance
    category_stats = db.session.query(
        Category.name,
        db.func.count(Quiz.id).label('quiz_count'),
        db.func.avg(Quiz.score).label('avg_score'),
        db.func.max(Quiz.score).label('best_score')
    ).join(Quiz).filter(Quiz.user_id == user.id)\
     .group_by(Category.id, Category.name).all()
    
    return render_template('profile.html', 
                         user=user, 
                         user_stats=user_stats, 
                         quiz_history=quiz_history,
                         category_stats=category_stats)

@app.route('/start_quiz', methods=['POST'])
@login_required
def start_quiz():
    data = request.get_json()
    category_id = data.get('category_id')
    difficulty = data.get('difficulty')
    
    if not all([category_id, difficulty]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Get random questions
    questions = Question.query.filter_by(
        category_id=category_id,
        difficulty=difficulty
    ).all()
    
    if len(questions) < 10:
        return jsonify({'error': 'Not enough questions for this category/difficulty'}), 400
    
    selected_questions = random.sample(questions, 10)
    
    # Create quiz session
    quiz = Quiz(
        user_id=session['user_id'],
        category_id=category_id,
        difficulty=difficulty,
        total_questions=10
    )
    db.session.add(quiz)
    db.session.commit()
    
    # Store quiz info in session
    session['quiz_id'] = quiz.id
    session['question_ids'] = [q.id for q in selected_questions]
    session['current_question'] = 0
    session['start_time'] = None
    
    return jsonify({'quiz_id': quiz.id, 'redirect': url_for('quiz_page')})

@app.route('/quiz')
@login_required
def quiz_page():
    if 'quiz_id' not in session:
        return redirect(url_for('index'))
    
    quiz = Quiz.query.get(session['quiz_id'])
    if not quiz or quiz.user_id != session['user_id']:
        return redirect(url_for('index'))
    
    return render_template('quiz.html', quiz=quiz)

@app.route('/get_question/<int:question_num>')
@login_required
def get_question(question_num):
    if 'quiz_id' not in session or question_num >= len(session['question_ids']):
        return jsonify({'error': 'Invalid question'}), 400
    
    # Verify quiz belongs to current user
    quiz = Quiz.query.get(session['quiz_id'])
    if not quiz or quiz.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    question_id = session['question_ids'][question_num]
    question = Question.query.get(question_id)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    question_data = {
        'id': question.id,
        'text': question.text,
        'type': question.question_type,
        'number': question_num + 1,
        'total': len(session['question_ids'])
    }
    
    if question.question_type == 'mcq':
        question_data['options'] = question.get_options()
    
    return jsonify(question_data)

@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    if 'quiz_id' not in session:
        return jsonify({'error': 'No active quiz'}), 400
    
    # Verify quiz belongs to current user
    quiz = Quiz.query.get(session['quiz_id'])
    if not quiz or quiz.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer', '').strip()
    time_taken = data.get('time_taken', 60)
    
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # Check if answer is correct
    is_correct = False
    correct_answer = question.correct_answer.strip()
    
    if question.question_type == 'true_false':
        is_correct = user_answer.lower() == correct_answer.lower()
    elif question.question_type == 'fill_blank':
        is_correct = user_answer.lower() == correct_answer.lower()
    elif question.question_type == 'mcq':
        is_correct = user_answer == correct_answer
    
    # Save answer
    quiz_answer = QuizAnswer(
        quiz_id=session['quiz_id'],
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct,
        time_taken=time_taken
    )
    db.session.add(quiz_answer)
    
    # Update quiz score
    if is_correct:
        quiz.score += 1
        db.session.commit()
    
    db.session.commit()
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': question.explanation
    })

@app.route('/finish_quiz', methods=['POST'])
@login_required
def finish_quiz():
    if 'quiz_id' not in session:
        return jsonify({'error': 'No active quiz'}), 400
    
    quiz = Quiz.query.get(session['quiz_id'])
    if not quiz or quiz.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    total_time = data.get('total_time', 0)
    
    quiz.time_taken = total_time
    quiz.completed_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'redirect': url_for('results', quiz_id=quiz.id)})

@app.route('/results/<int:quiz_id>')
@login_required
def results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Ensure user can only view their own results
    if quiz.user_id != session['user_id']:
        flash('You can only view your own quiz results.')
        return redirect(url_for('index'))
    
    answers = QuizAnswer.query.filter_by(quiz_id=quiz_id).all()
    
    # Clear session
    session.pop('quiz_id', None)
    session.pop('question_ids', None)
    session.pop('current_question', None)
    
    return render_template('results.html', quiz=quiz, answers=answers)

# Admin Routes
@app.route('/admin')
def admin_login():
    if session.get('admin'):
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # if username == app.config['ADMIN_USERNAME'] and check_password_hash(app.config['ADMIN_PASSWORD_HASH'], password):
    if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD_HASH']:
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    
    flash('Invalid credentials')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    categories = Category.query.all()
    questions_count = Question.query.count()
    quizzes_count = Quiz.query.count()
    
    return render_template('admin/dashboard.html', 
                         categories=categories,
                         questions_count=questions_count,
                         quizzes_count=quizzes_count)

@app.route('/admin/add_question')
def admin_add_question():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    categories = Category.query.all()
    return render_template('admin/add_question.html', categories=categories)

@app.route('/admin/save_question', methods=['POST'])
def admin_save_question():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = request.get_json()
    
    question = Question(
        text=data['text'],
        question_type=data['type'],
        difficulty=data['difficulty'],
        correct_answer=data['correct_answer'],
        explanation=data.get('explanation', ''),
        category_id=data['category_id']
    )
    
    if data['type'] == 'mcq':
        question.set_options(data['options'])
    
    db.session.add(question)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/categories')
@login_required
def get_categories():
    sport_id = request.args.get('sport_id')
    if not sport_id:
        return jsonify([]), 400
    
    categories = Category.query.filter_by(sport_id=sport_id).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

@app.route('/admin/reports')
def admin_reports():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    # Category statistics
    category_stats = db.session.query(
        Category.name,
        Sport.name.label('sport_name'),
        db.func.count(Quiz.id).label('quiz_count'),
        db.func.avg(Quiz.score).label('avg_score')
    ).join(Quiz).join(Sport).group_by(Category.id, Category.name, Sport.name).all()
    
    # User activity
    users = User.query.all()
    
    return render_template('admin/reports.html', category_stats=category_stats, users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)