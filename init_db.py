from app import app
from models import db, Sport, Category, Question, User

def init_database():
    with app.app_context():
        # Drop and create all tables
        db.drop_all()
        db.create_all()
        
        # Create a demo user
        demo_user = User(
            username='demo',
            email='demo@cricketquiz.com',
            full_name='Demo User'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        
        # Create sports
        sports_data = [
            {'name': 'Cricket', 'description': 'Questions about cricket'},
            {'name': 'Football', 'description': 'Questions about football'},
            {'name': 'Hockey', 'description': 'Questions about hockey'},
        ]
        
        for sport_data in sports_data:
            sport = Sport(**sport_data)
            db.session.add(sport)
        
        db.session.commit()
        
        # Create categories for cricket
        categories_data = [
            {'name': 'World Cup', 'description': 'Cricket World Cup related questions', 'sport_name': 'Cricket'},
            {'name': 'Batting', 'description': 'Batting techniques, records, and strategies', 'sport_name': 'Cricket'},
            {'name': 'Bowling', 'description': 'Bowling techniques, types, and records', 'sport_name': 'Cricket'},
            {'name': 'Fielding', 'description': 'Fielding positions and techniques', 'sport_name': 'Cricket'},
            {'name': 'History', 'description': 'Cricket history and legends', 'sport_name': 'Cricket'},
            {'name': 'Rules', 'description': 'Cricket rules and regulations', 'sport_name': 'Cricket'},
        ]
        
        for cat_data in categories_data:
            sport = Sport.query.filter_by(name=cat_data['sport_name']).first()
            category = Category(
                name=cat_data['name'],
                description=cat_data['description'],
                sport_id=sport.id
            )
            db.session.add(category)
        
        db.session.commit()
        
        # Sample questions for cricket
        sample_questions = [
            {
                'text': 'Which country won the ICC Cricket World Cup 2019?',
                'question_type': 'mcq',
                'difficulty': 'easy',
                'options': ['England', 'New Zealand', 'Australia', 'India'],
                'correct_answer': 'England',
                'explanation': 'England won their first Cricket World Cup in 2019',
                'category': 'World Cup'
            },
            {
                'text': 'The maximum number of overs in a T20 match is 20 per team.',
                'question_type': 'true_false',
                'difficulty': 'easy',
                'correct_answer': 'True',
                'explanation': 'T20 cricket has exactly 20 overs per team',
                'category': 'Rules'
            },
            {
                'text': 'Who holds the record for highest individual score in Test cricket?',
                'question_type': 'fill_blank',
                'difficulty': 'medium',
                'correct_answer': 'Brian Lara',
                'explanation': 'Brian Lara scored 400* against England in 2004',
                'category': 'Batting'
            },
            {
                'text': 'Which bowler has taken the most wickets in Test cricket?',
                'question_type': 'mcq',
                'difficulty': 'medium',
                'options': ['Shane Warne', 'Muttiah Muralitharan', 'James Anderson', 'Anil Kumble'],
                'correct_answer': 'Muttiah Muralitharan',
                'explanation': 'Muttiah Muralitharan has 800 Test wickets, the most in cricket history',
                'category': 'Bowling'
            },
            {
                'text': 'A cricket ball has 6 seams.',
                'question_type': 'true_false',
                'difficulty': 'easy',
                'correct_answer': 'True',
                'explanation': 'A cricket ball is made with 6 seams of stitching',
                'category': 'Rules'
            },
            {
                'text': 'Which Indian captain led the team to their first World Cup victory?',
                'question_type': 'fill_blank',
                'difficulty': 'medium',
                'correct_answer': 'Kapil Dev',
                'explanation': 'Kapil Dev captained India to their first World Cup win in 1983',
                'category': 'World Cup'
            },
            {
                'text': 'What is the maximum number of players that can be on the field for the fielding team?',
                'question_type': 'mcq',
                'difficulty': 'easy',
                'options': ['10', '11', '12', '9'],
                'correct_answer': '11',
                'explanation': 'The fielding team has 11 players on the field',
                'category': 'Rules'
            },
            {
                'text': 'A batsman can be out "handled the ball".',
                'question_type': 'true_false',
                'difficulty': 'hard',
                'correct_answer': 'False',
                'explanation': 'This law was removed in 2017 and is now part of "obstructing the field"',
                'category': 'Rules'
            },
            {
                'text': 'Who scored the fastest century in ODI cricket?',
                'question_type': 'fill_blank',
                'difficulty': 'hard',
                'correct_answer': 'AB de Villiers',
                'explanation': 'AB de Villiers scored a century in 31 balls against West Indies in 2015',
                'category': 'Batting'
            },
            {
                'text': 'Which field position is closest to the batsman on the leg side?',
                'question_type': 'mcq',
                'difficulty': 'medium',
                'options': ['Short leg', 'Square leg', 'Mid-wicket', 'Fine leg'],
                'correct_answer': 'Short leg',
                'explanation': 'Short leg is the closest fielding position to the batsman on the leg side',
                'category': 'Fielding'
            }
        ]
        
        for q_data in sample_questions:
            category = Category.query.filter_by(name=q_data['category']).first()
            question = Question(
                text=q_data['text'],
                question_type=q_data['question_type'],
                difficulty=q_data['difficulty'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                category_id=category.id
            )
            
            if 'options' in q_data:
                question.set_options(q_data['options'])
            
            db.session.add(question)
        
        db.session.commit()
        print("Database initialized successfully!")
        print("Demo user created - Username: 'demo', Password: 'demo123'")

if __name__ == '__main__':
    init_database()