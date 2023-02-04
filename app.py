# Flask Web Application for Quiz Game 
# This code implements the route for the result page, which displays the user's score

from flask import Flask, render_template, request
import json

# Load the questions from quests.json file
with open("quests.json", "r") as file:
    quests=json.load(file)

# Create Flask application
app = Flask(__name__)

# Custom class for Quiz Game that inherits from Flask
class Quizgame(Flask):
    def __init__(self, name, quests):
        super().__init__(name)
        self.quests = quests
        self.total = len(self.quests)
        self.answers=[]
        self.user_answers=[]
        self.correct = 0

    # Method to retrieve correct answers from quests
    def correct_answer(self):
        self.answers=[]
        for answer in self.quests:
            self.answers.append(answer["answer"].title())
        return self.answers

# Create an instance of Quizgame class
quizgame = Quizgame(__name__, quests)

# Route for the index page
@quizgame.route("/")
def index():
    quizgame.correct = 0
    return render_template("index.html")

# Route for the question page
@quizgame.route("/question", methods=["GET", "POST"])
def question():
    return render_template("game_brain.html", quests=quests, enumerate=enumerate)

# Route for the result page
@quizgame.route("/result", methods=["GET", "POST"])
def result():
    quizgame.user_answers=[]
    correct_answers = quizgame.correct_answer()
    
    # Retrieve user's answers from the form submissions
    for i in range(len(correct_answers)):
        user_answer = request.form.get(str(f"responses{i}"))
        
        # Validate the answer
        if user_answer != "None":
            quizgame.user_answers.append(str(user_answer).title())
        else:
            quizgame.user_answers.append("invalid_answer")

    # Calculate the number of correct answers
    for i in range(len(correct_answers)):
        if quizgame.user_answers[i] == correct_answers[i]:
            quizgame.correct += 1

    # Render the result page with user's score
    return f'{render_template("result.html", score=quizgame.correct, total=len(correct_answers))}'

# Run the application if executed as the main script
if __name__ == "__main__":
    quizgame.run(debug=True)
