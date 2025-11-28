from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import datetime
import os
import json
import random
from dotenv import load_dotenv
import logging

from models import db  # Import db from models.py

# Load environment variables first
load_dotenv()

# Create Flask app instance
# Use /tmp for instance path on Vercel/serverless (read-only filesystem), normal path locally
# Check for multiple serverless indicators
is_serverless = (
    os.getenv('VERCEL') or
    os.getenv('AWS_LAMBDA_FUNCTION_NAME') or
    os.getenv('FUNCTION_NAME') or
    not os.access('.', os.W_OK)  # Check if current directory is writable
)

if is_serverless:
    app = Flask(__name__, instance_path='/tmp')
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_USERNAME'] = os.getenv('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD_HASH'] = os.getenv('ADMIN_PASSWORD_HASH', 'admin')

# Add connection pooling for better performance in production/serverless
if is_serverless or os.getenv('FLASK_ENV') == 'production':
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

migrate = Migrate()

def create_app(host=None, port=None):
    # Initialize the app with SQLAlchemy using the db from models.py
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after app initialization to avoid circular imports
    with app.app_context():
        from models import User, Sport, Category, Question, Quiz, QuizAnswer, Settings

        # Logging configuration - use stdout on serverless, file locally
        if is_serverless:
            # On serverless platforms, log to stdout (visible in platform logs)
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler()]
            )
        else:
            # Local development: log to file
            logging.basicConfig(
                filename='app.log',
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
        

        # Authentication decorator
        def login_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'user_id' not in session:
                    return redirect(url_for('login'))
                return f(*args, **kwargs)
            return decorated_function



        # Register routes
        @app.route('/')
        def index():
            if 'user_id' in session:
                user = User.query.get(session['user_id'])
                sports = Sport.query.all()
                categories = Category.query.filter(Category.question_count>0).all()
                return render_template('index.html', user=user, sports=sports, categories=categories)
            return redirect(url_for('login'))

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                full_name = request.form['full_name']
                
                if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                    flash('Username or email already exists')
                    return redirect(url_for('register'))
                
                user = User(username=username, email=email, full_name=full_name)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Registration successful! Please log in.')
                return redirect(url_for('login'))
            
            return render_template('auth/register.html')

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                username = data.get('username')
                password = data.get('password')
                
                if not username or not password:
                    return jsonify({'error': 'Username and password are required'}), 400
                
                user = User.query.filter_by(username=username).first()
                if user and user.check_password(password):
                    session['user_id'] = user.id
                    session['username'] = user.username
                    session['full_name'] = user.full_name
                    user.last_login = datetime.utcnow()
                    db.session.commit()
                    return jsonify({'redirect': url_for('index')}), 200
                return jsonify({'error': 'Invalid username or password'}), 401
            
            return render_template('auth/login.html')

        @app.route('/logout')
        def logout():
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('full_name', None)
            return redirect(url_for('login'))

        @app.route('/admin', methods=['GET', 'POST'])
        def admin_login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                
                # if username == app.config['ADMIN_USERNAME'] and check_password_hash(app.config['ADMIN_PASSWORD_HASH'], password):
                if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD_HASH']:
                    session['admin'] = True
                    return redirect(url_for('admin_dashboard'))
                flash('Invalid credentials')
            
            return render_template('admin/login.html')

        @app.route('/admin/logout')
        def admin_logout():
            session.pop('admin', None)
            return redirect(url_for('admin_login'))

        @app.route('/admin/dashboard')
        def admin_dashboard():
            if not session.get('admin'):
                return redirect(url_for('admin_login'))
            
            total_users = User.query.count()
            total_quizzes = Quiz.query.count()
            total_questions = Question.query.count()
            quiz_length_setting = Settings.query.filter_by(key='default_quiz_length').first()
            categories = Category.query.all()
            return render_template('admin/dashboard.html', 
                                 total_users=total_users,
                                 total_quizzes=total_quizzes,
                                 total_questions=total_questions,
                                 categories=categories,
                                 quiz_length=quiz_length_setting.value if quiz_length_setting else 10)

        @app.route('/admin/settings', methods=['GET', 'POST'])
        def admin_settings():
            if not session.get('admin'):
                return redirect(url_for('admin_login'))
            
            if request.method == 'POST':
                quiz_length = request.form.get('quiz_length', type=int)
                if quiz_length and quiz_length > 0:
                    setting = Settings.query.filter_by(key='default_quiz_length').first()
                    if not setting:
                        setting = Settings(key='default_quiz_length', value=str(quiz_length), description='Default number of questions per quiz')
                        db.session.add(setting)
                    else:
                        setting.value = str(quiz_length)
                    db.session.commit()
                    flash('Quiz length updated successfully!')
                    return redirect(url_for('admin_dashboard'))
                flash('Invalid quiz length')
            
            quiz_length_setting = Settings.query.filter_by(key='default_quiz_length').first()
            return render_template('admin/settings.html', quiz_length=quiz_length_setting.value if quiz_length_setting else 10)

        @app.route('/admin/add_question', methods=['GET', 'POST'])
        def add_question():
            if not session.get('admin'):
                return redirect(url_for('admin_login'))
            
            if request.method == 'POST':
                text = request.form['text']
                question_type = request.form['question_type']
                difficulty = request.form['difficulty']
                correct_answer = request.form['correct_answer']
                explanation = request.form['explanation']
                category_id = request.form['category_id']
                
                options = []
                if question_type == 'mcq':
                    options = [
                        request.form.get('option1', ''),
                        request.form.get('option2', ''),
                        request.form.get('option3', ''),
                        request.form.get('option4', '')
                    ]
                    options = [opt for opt in options if opt]
                
                question = Question(
                    text=text,
                    question_type=question_type,
                    difficulty=difficulty,
                    correct_answer=correct_answer,
                    explanation=explanation,
                    category_id=category_id
                )
                if options:
                    question.set_options(options)
                
                db.session.add(question)
                db.session.commit()
                flash('Question added successfully!')
                return redirect(url_for('admin_dashboard'))
            # sports = Sport.query.filter(Sport.deleted_at.isnot(None)).all()
            sports = Sport.query.all()
            # categories = Category.query.all()
            return render_template('admin/add_question.html', sports = sports)

        @app.route('/admin/save_question', methods=['POST'])
        def admin_save_question():
            if not session.get('admin'):
                return redirect(url_for('admin_login'))
            
            data = request.get_json()
            category_id = data['category_id']
            sport_id = data['sport_id']
            question = Question(
                text=data['text'],
                question_type=data['type'],
                difficulty=data['difficulty'],
                correct_answer=data['correct_answer'],
                explanation=data.get('explanation', ''),
                category_id=category_id,
                sport_id =sport_id
            )
            
            if data['type'] == 'mcq':
                question.set_options(data['options'])
            
            db.session.add(question)

            category = Category.query.get(category_id)
            category.updated_at = datetime.utcnow()
            category.question_count = (category.question_count or 0) + 1
            db.session.add(category)

            db.session.commit()
            
            return jsonify({'success': True})



        @app.route('/profile')
        def profile():
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            stats = user.get_stats()
            
            # Query for category-wise stats
            category_stats = []
            quizzes = Quiz.query.filter_by(user_id=user.id).all()
            if quizzes:
                category_counts = {}
                for quiz in quizzes:
                    cat_name = quiz.category.name
                    category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
                    total_score = sum(q.score for q in quizzes if q.category.name == cat_name)
                    total_questions = sum(q.total_questions for q in quizzes if q.category.name == cat_name)
                    best_score = max((q.score for q in quizzes if q.category.name == cat_name), default=0)
                    avg_score = (total_score / total_questions * 100) if total_questions > 0 else 0
                
                for cat_name, count in category_counts.items():
                    category_stats.append({
                        'name': cat_name,
                        'quiz_count': count,
                        'avg_score': avg_score,
                        'best_score': best_score
                    })
            
            # Paginate quiz history
            page = request.args.get('page', 1, type=int)
            quiz_history = Quiz.query.filter_by(user_id=user.id).order_by(Quiz.completed_at.desc()).paginate(page=page, per_page=5, error_out=False)
            print('quiz_history',quiz_history)
            return render_template('profile.html', user=user, stats=stats, category_stats=category_stats, quiz_history=quiz_history)
    
        @app.route('/start_quiz', methods=['GET', 'POST'])
        def start_quiz():
            if 'user_id' not in session:
                return redirect(url_for('login'))
            # data = request.get_json()
            
            category_id = request.form.get('category_id')
            difficulty = request.form.get('difficulty')

            # difficulty = data.get('difficulty')
            
            if not all([category_id, difficulty]):
                flash('Missing required fields')
                return redirect(url_for('index'))
                # return jsonify({'error': 'Missing required fields'}), 400
            
            quiz_length_setting = Settings.query.filter_by(key='default_quiz_length').first()
            quiz_length = int(quiz_length_setting.value) if quiz_length_setting else 10
            questions = Question.query.filter_by(category_id=category_id, difficulty=difficulty).all()
            if len(questions) < quiz_length:
                flash('Not enough questions available for this category and difficulty.')
                return redirect(url_for('index'))
            
            questions = random.sample(questions, quiz_length)
            if len(questions) != quiz_length:
                print(f"Warning: Only {len(questions)} questions sampled, expected {quiz_length}")
    
            quiz = Quiz(
                user_id=session['user_id'],
                category_id=category_id,
                difficulty=difficulty,
                total_questions=quiz_length
            )
            db.session.add(quiz)
            db.session.commit()
            
            session['quiz_id'] = quiz.id
            session['questions'] = [q.id for q in questions]
            session['current_question'] = 0
            session['score'] = 0
            session['answers'] = []
            session['start_time'] = datetime.utcnow().isoformat()
            
            return redirect(url_for('quiz_question', question_num=1))

        @app.route('/quiz/<int:question_num>', methods=['GET', 'POST'])
        def quiz_question(question_num):
            if 'user_id' not in session or 'quiz_id' not in session:
                return redirect(url_for('login'))
            
            if question_num < 1 or question_num > len(session['questions']):
                return redirect(url_for('quiz_result'))
            
            question_id = session['questions'][question_num - 1]
            question = Question.query.get(question_id)
            
            if not question:
                flash('Question not found')
                return redirect(url_for('quiz_result'))
            total_questions = len(session['questions'])
            progress = (question_num / total_questions) * 100
            
            if request.method == 'POST':
                user_answer = request.form.get('answer')
                start_time = datetime.fromisoformat(session['start_time'])
                time_taken = int((datetime.utcnow() - start_time).total_seconds())
                
                is_correct = user_answer == question.correct_answer
                if is_correct:
                    session['score'] += 1
                
                quiz_answer = QuizAnswer(
                    quiz_id=session['quiz_id'],
                    question_id=question.id,
                    user_answer=user_answer,
                    is_correct=is_correct,
                    time_taken=time_taken
                )
                db.session.add(quiz_answer)
                session['answers'].append({
                    'question_id': question.id,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'time_taken': time_taken
                })
                db.session.commit()
            
                session['start_time'] = datetime.utcnow().isoformat()

                if request.form.get('action') == 'next' and question_num < total_questions:
                    return redirect(url_for('quiz_question', question_num=question_num + 1))
                elif request.form.get('action') == 'submit' or question_num == total_questions:
                    print('debug check')
                    return quiz_submit()
                    # return redirect(url_for('quiz_result'))
            
            return render_template('quiz_question.html',
                                 question=question,
                                 question_num=question_num,
                                 total_questions=total_questions,
                                 progress=progress)

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
            print('is_correct',is_correct)
            # Update quiz score
            if is_correct:
                quiz.score += 1
                print('checking')
                db.session.commit()
                print('checking123')
            
            db.session.commit()
            
            return jsonify({
                'correct': is_correct,
                'correct_answer': correct_answer,
                'explanation': question.explanation
            })


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



        @app.route('/quiz/submit', methods=['POST'])
        def quiz_submit():
            if 'user_id' not in session or 'quiz_id' not in session:
                return redirect(url_for('login'))
            
            quiz = Quiz.query.get(session['quiz_id'])
            if not quiz:
                flash('Quiz not found')
                return redirect(url_for('index'))
            print('checkkkkkkkkkk', session['score'])
            quiz.score = session['score']
            quiz.time_taken = sum(answer['time_taken'] for answer in session['answers'])
            # print('checkkkkkkkkkkinggggg', quiz['time_taken'])
            quiz.completed_at = datetime.utcnow()
            db.session.commit()
            
            return redirect(url_for('quiz_result'))

        @app.route('/results/<int:quiz_id>')
        def results(quiz_id):
            quiz = Quiz.query.get_or_404(quiz_id)
            if quiz.user_id != session.get('user_id'):
                return redirect(url_for('login'))
            
            answers = QuizAnswer.query.filter_by(quiz_id=quiz_id).all()
            detailed_results = []
            for answer in answers:
                question = Question.query.get(answer.question_id)
                detailed_results.append({
                    'question_text': question.text,
                    'user_answer': answer.user_answer,
                    'correct_answer': question.correct_answer,
                    'is_correct': answer.is_correct,
                    'time_taken': answer.time_taken,
                    'explanation': question.explanation
                })
            
            return render_template('results.html', quiz=quiz, detailed_results=detailed_results)

        @app.route('/categories')
        @login_required
        def get_categories():
            sport_id = request.args.get('sport_id')
            if not sport_id:
                return jsonify([]), 400
            
            categories = Category.query.filter_by(sport_id=sport_id).all()
            return jsonify([{'id': c.id, 'name': c.name} for c in categories])


        
        @app.route('/quiz/result')
        def quiz_result():
            if 'user_id' not in session or 'quiz_id' not in session:
                return redirect(url_for('login'))
            
            quiz = Quiz.query.get(session['quiz_id'])
            if not quiz:
                flash('Quiz not found')
                return redirect(url_for('index'))
            
            answers = session.get('answers', [])
            detailed_results = []
            for answer in answers:
                question = Question.query.get(answer['question_id'])
                detailed_results.append({
                    'question_text': question.text,
                    'user_answer': answer['user_answer'],
                    'correct_answer': question.correct_answer,
                    'is_correct': answer['is_correct'],
                    'time_taken': answer['time_taken'],
                    'explanation': question.explanation
                })
            
            score_percentage = (quiz.score / quiz.total_questions) * 100 if quiz.total_questions > 0 else 0
            
            session.pop('quiz_id', None)
            session.pop('questions', None)
            session.pop('current_question', None)
            session.pop('score', None)
            session.pop('answers', None)
            session.pop('start_time', None)
            
            return render_template('quiz_result.html',
                                 score=quiz.score,
                                 total_questions=quiz.total_questions,
                                 score_percentage=score_percentage,
                                 detailed_results=detailed_results,
                                 category=quiz.category.name)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)