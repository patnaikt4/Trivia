import html
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import requests
import random
import time

# Configuring Software
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disabling a feature in SQLAlchemy
app.config['SECRET_KEY'] = 'your_secret_key' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Defining a database for a user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # a primary key to identify users by
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    scores = db.relationship('Score', backref='user', lazy=True) # Relationship between this and the Score below

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True) # a primary key to identify scores by
    score = db.Column(db.Integer, nullable=False) # storing scores as ints
    total = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)  # New column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user_id's so we can tell which user the scores belong to


# URLS for the API's that contain questions of all three difficulties
TRIVIA_EASY_URL = "https://opentdb.com/api.php?amount=10&difficulty=easy"
TRIVIA_MEDIUM_URL = "https://opentdb.com/api.php?amount=10&difficulty=medium"
TRIVIA_HARD_URL = "https://opentdb.com/api.php?amount=10&difficulty=hard"



def fetch_questions(difficulty='easy', retries=3, delay=2): 
    
    # Classifying difficulty of questions to fetch
    if difficulty == 'easy':
        url = TRIVIA_EASY_URL
    elif difficulty == 'medium':
        url = TRIVIA_MEDIUM_URL
    else:
        url = TRIVIA_HARD_URL
    
    # Attempt this a "retries" amount of times (3 usually)
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('results', [])
            formatted_questions = []
            for idx, question in enumerate(data, start=1):
                formatted_questions.append({
                    "id": idx,
                    "question": html.unescape(question["question"]),
                    "correct_answer": html.unescape(question["correct_answer"]),
                    "incorrect_answers": [html.unescape(ans) for ans in question["incorrect_answers"]]
                })
            print(f"Fetched {len(formatted_questions)} questions for difficulty '{difficulty}'")
            return formatted_questions
        
        # If we get the error corresponding to too many requests
        elif response.status_code == 429:
            print(f"Rate-limited (429). Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})") 
            time.sleep(delay)  # Wait before retrying
            delay *= 2  # Exponential backoff
    
    # If all else failes,
    print(f"Failed to fetch questions for difficulty '{difficulty}' after {retries} retries.") 
    return []


@app.route("/", methods=["GET", "POST"])
def index():
    if 'user_id' not in session:  # If the user isn't logged in, send them back to the login page
        return redirect(url_for('login'))

    # POST is when handling submissions
    if request.method == "POST":
        # Processing questions
        questions = session.get('questions', []) # Get the questions. If fails, returns empty array
        score = 0
        for question in questions: # Looping through  questions
            user_answer = request.form.get(f"question-{question['id']}")
            if user_answer == question["correct_answer"]: 
                score += 1 # If answer is right, increment score

        # Save score to database
        user_id = session.get('user_id') # Get the user_id of the user
        difficulty = session.get('difficulty', '--') # Get the difficulty
        if user_id and difficulty != '--': # As long as both aren't default values
            new_score = Score(score=score, total=len(questions), difficulty=difficulty, user_id=user_id) # Create a score object 
            db.session.add(new_score)
            db.session.commit()

        session['score'] = score
        session['total'] = len(questions)
        return redirect(url_for("result"))

    # Handle GET request for quiz selection
    
    # Getting the difficulty from the URL
    difficulty = request.args.get("difficulty", "--")

    # If default difficulty is selected
    if difficulty == "--":
        session['difficulty'] = None  # Reset session difficulty
        questions = []
        total_questions = 0
        return render_template(
            "index.html",
            questions=questions,
            difficulty=difficulty,
            total_questions=total_questions,
            message="Please choose a difficulty level."
        )

    # If a valid difficulty is chosen, update the session and fetch questions
    if session.get('difficulty') != difficulty:
        session['difficulty'] = difficulty
        questions = fetch_questions(difficulty)  # Fetch questions for the selected difficulty
        session['questions'] = questions
    else:
        questions = session.get('questions', []) # If the difficulty hasn't changed, keep the same questions

    total_questions = len(questions)
    return render_template(
        "index.html",
        questions=questions,
        difficulty=session.get('difficulty'),
        total_questions=total_questions
    )


@app.route("/result", methods=["GET", "POST"])
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Make sure user is logged in

    # Retrieve score and total from the session
    score = session.get('score', 0)
    total_questions = session.get('total', 0)

    return render_template('result.html', score=score, total=total_questions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle Processing of info
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') # using function from security library imported


        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return "Username already exists. Please choose another."

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handling Form Submissions
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password): # If the login exists in the database
            session['user_id'] = user.id 
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "error")  # Flash the error message
            return redirect(url_for('login'))  # Redirect back to the login page

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login')) # If not logged in, send back to login

    user_id = session.get('user_id') # Getting the user_id
    user = User.query.get(user_id)
    if not user: # Checking if entry exists
        return redirect(url_for('login'))

    # Fetching scores by difficulty
    difficulties = ['easy', 'medium', 'hard']
    stats = {}
    scores_data = []  # For the first data viz
    performance_data = {difficulty: [] for difficulty in difficulties}  # For the second data viz

    # Tracking max. num of quizzes by difficulty
    max_quizzes = 0
    for difficulty in difficulties:
        scores = Score.query.filter_by(user_id=user_id, difficulty=difficulty).order_by(Score.id).all()
        total_quizzes = len(scores) # Used in data visualizations
        max_quizzes = max(max_quizzes, total_quizzes)  # Update the maximum quizzes count

        total_score = sum(score.score for score in scores)
        average_score = total_score / total_quizzes if total_quizzes > 0 else 0 # returning the average score for the specified difficulty

        # Populate stats for the stats cards
        stats[difficulty] = {
            'total_quizzes': total_quizzes,
            'total_score': total_score,
            'average_score': average_score,
        }

        # Populate scores_data for the first graph
        scores_data.append({
            "difficulty": difficulty,
            "total_quizzes": total_quizzes,
            "total_score": total_score,
            "average_score": average_score,
        })

        # Second graph
        performance_data[difficulty] = [score.score for score in scores] + [None] * (max_quizzes - total_quizzes)

    # Debugging code used while in development
    print("Stats:", stats)
    print("Scores Data:", scores_data)
    print("Performance Data:", performance_data)
    print("Max Quizzes:", max_quizzes)

    return render_template(
        'analytics.html',
        user=user,
        stats=stats,
        scores_data=scores_data,
        performance_data=performance_data,
        max_quizzes=max_quizzes
    )

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

