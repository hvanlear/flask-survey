from flask import Flask, request, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def show_homepage():
    return render_template('home.html')


@app.route('/sat_surv')
def show_surv_home():
    question = 0
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('sat_surv.html', title=title, instructions=instructions, question=question)


@app.route('/sat_surv/question/<int:question_num>', methods=['GET', 'POST'])
def show_question(question_num):
    next_question = question_num + 1
    if next_question > len(satisfaction_survey.questions):
        return redirect('/thanks')
    question = satisfaction_survey.questions[question_num].question
    choices = satisfaction_survey.questions[question_num].choices

    if request.method == 'POST':
        answer = request.form["choice"]
        responses.append(answer)
        return redirect(f"/sat_surv/question/{question_num}")

    return render_template('question.html', question_num=question_num, question=question, choices=choices, next_question=next_question)


@app.route('/thanks')
def show_thanks_page():
    print(responses)
    return render_template('thanks.html')
