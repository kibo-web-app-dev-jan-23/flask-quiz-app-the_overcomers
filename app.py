from flask import Flask, render_template, request
import json

with open("quests.json", "r") as file:
    quests=json.load(file)
app = Flask(__name__)

class Quizgame(Flask):
    def __init__(self, name, quests):
        super().__init__(name)
        self.quests = quests
        self.total = len(self.quests)
        self.answers=[]
        self.user_answers=[]
        self.correct = 0

    def correct_answer(self):
        self.answers=[]
        for answer in self.quests:
            self.answers.append(answer["answer"].title())
        return self.answers


quizgame = Quizgame(__name__, quests)

@quizgame.route("/")
def index():
    return render_template("index.html")

@quizgame.route("/question", methods=["GET", "POST"])
def question():
    return render_template("game_brain.html", quests=quests, enumerate=enumerate)

@quizgame.route("/result", methods=["GET", "POST"])
def result():
    correct_answers = quizgame.correct_answer()
    for i in range(len(correct_answers)):
        user_answer = request.form["responses"]
        try:
            # check if the user has provided an answer
            if user_answer:
                quizgame.user_answers.append(str(user_answer).title())
        except KeyError:
            quizgame.user_answers.append("")

    for i in range(len(correct_answers)):
        if quizgame.user_answers[i] == correct_answers[i]:
            quizgame.correct += 1


    return f'{render_template("result.html", score=quizgame.correct, total=len(correct_answers))}'

   

if __name__ == "__main__":
    quizgame.run(debug=True)
