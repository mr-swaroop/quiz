from flask import Flask, request,render_template,redirect,url_for

import pandas as pd
import random
from pymongo import MongoClient

app = Flask(__name__)

host = "ocdb.app"
port = 5050
database = "db_42wrhgtke" # your database
username = "user_42wrhgtke" # your username
password = "p42wrhgtke" # your password
 
connection_string = f"mongodb://{username}:{password}@{host}:{port}/{database}"
my_client = MongoClient(connection_string)
my_db = my_client[database]
login = my_db["login_details"]


@app.route('/',methods=['GET',"POST"])
def login_form():
    if request.method == 'POST':
        name=request.form["user_id"]
        password=request.form["password"]
        user_details=login.find_one({'name': name ,"password": password})
        if user_details:
            return render_template("login_sucess.html")       
        else:
            return render_template("login.html", data = f"{name} has no account ")      
    else:
        return render_template('login.html')

    
@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method == 'POST':
        name=request.form["user_id"]
        password=request.form["password"]
        login.insert_one({"name":name,"password":password})
        return render_template("register.html", name = name)
    else:
        return render_template('register.html')

# for bits exam  

# Load questions from CSV
def load_questions():
    questions = []
    data = pd.read_csv('exam.csv', encoding='ISO-8859-1')
    for _, row in data.iterrows():
        questions.append({
            'question': row['QUESTIONS'],
            'choices': [f"A . {row['OPTION-A']}", f"B . {row['OPTION-B']}", f"C . {row['OPTION-C']}", f"D . {row['OPTION-D']}"],
            'answer': row['CORRECT ANSWER']
        })
    return questions
@app.route('/quiz')
def quiz():
    questions = load_questions()
    # Select 20 random questions
    selected_questions = random.sample(questions, min(20, len(questions)))
    return render_template('quiz.html', questions=selected_questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = load_questions()
    score = 0
    # Calculate score
    for question in questions:
        ua=str(request.form.get(question['question']))
        print(ua)
        user_answer = ua[0]
        correct_answer = str(question['answer'])
        if user_answer == correct_answer:
            score += 1

    return render_template('result.html', score=score, total=20)

app.run(debug=True)