"""
This is a multiple choice trivia game that keeps the score of the user. The API is from "The Trivia API".
"""
import requests
import tkinter as tk
import random as r

SCORE_FILE = 'score.txt'
API_URL = 'https://the-trivia-api.com/api/questions/'
WRAP_LEN = 450
PADY = 10
CORRECT_COLOR = '#28a745'
INCORRECT_COLOR = '#dc3545'


class Questions:
    def __init__(self) -> None:
        self.questions_queue = []
        self.questions_asked = []
        self.current_question = {}
        self.trivia = ''
        self.correct_answer = ''
        self.incorrect_answers = []
        self.answers_shuffled = []
        self.score = 0
        self.highest_score = 0
        self.highest_score_questions = 0
        self.get_highest_score()

    def fetch_questions(self) -> None:
        """
        Fetches the questions from the trivia API
        :return: None
        """
        response = requests.get(API_URL)
        response.raise_for_status()
        tmp_questions = response.json()
        self.questions_queue = [que for que in tmp_questions if que['id'] not in self.questions_asked]
        print(f'fetched {len(self.questions_queue)} new questions.')

    def initialize_question(self) -> None:
        """
        Initializes a question and its multiple choice answers
        :return: None
        """
        if not self.questions_queue:
            self.fetch_questions()
        to_ask = self.questions_queue.pop()
        self.current_question = to_ask
        self.questions_asked.append(self.current_question['id'])
        self.trivia = self.current_question['question']
        self.correct_answer = self.current_question['correctAnswer']
        self.incorrect_answers = self.current_question['incorrectAnswers']
        self.answers_shuffled = self.incorrect_answers + [self.correct_answer]
        r.shuffle(self.answers_shuffled)

    def check_answer(self, answer: str) -> bool:
        """
        Checks if the answer is the correct one
        :param answer: The answer chosen by the user.
        :return: True if correct, False otherwise
        """
        if answer == self.correct_answer:
            self.score += 1
            return True
        return False

    def get_highest_score(self) -> None:
        """
        Gets the highest score from the file where it's kept.
        :return: None
        """
        try:
            with open(SCORE_FILE) as score_file:
                self.highest_score_questions, self.highest_score = score_file.read().split('/')
        except FileNotFoundError:
            self.highest_score_questions, self.highest_score = 0, 0

    def set_highest_score(self) -> None:
        """
        Sets the highest score on the file where it is saved and assigns the variables on the class.
        :return: None
        """
        try:
            with open(SCORE_FILE, 'w') as score_file:
                score_file.write(f'{len(self.questions_asked)}/{self.score}')
        except FileNotFoundError:
            pass
        finally:
            self.highest_score_questions, self.highest_score = len(self.questions_asked), self.score


def check_answer(answer: str) -> None:
    """
    It takes care of checking the answer from the button the user clicked.
    :param answer: The answer from the button.
    :return: None
    """
    correct = questions.check_answer(answer)
    correct_incorrect.config(text='Correct!' if correct else 'Incorrect',
                             fg=CORRECT_COLOR if correct else INCORRECT_COLOR)
    previous_answer.config(text=f'Previous answer: {questions.correct_answer}')

    score.config(text=f'Score: {questions.score} from {len(questions.questions_asked)}')
    questions.get_highest_score()
    if questions.score > int(questions.highest_score):
        questions.set_highest_score()
        highest_score.config(
            text=f'Highest score: {questions.highest_score} from {questions.highest_score_questions} questions')

    questions.initialize_question()
    question.config(text=questions.trivia)
    answer_1_button.config(text=questions.answers_shuffled[0],
                           command=lambda: check_answer(questions.answers_shuffled[0]))
    answer_2_button.config(text=questions.answers_shuffled[1],
                           command=lambda: check_answer(questions.answers_shuffled[1]))
    answer_3_button.config(text=questions.answers_shuffled[2],
                           command=lambda: check_answer(questions.answers_shuffled[2]))
    answer_4_button.config(text=questions.answers_shuffled[3],
                           command=lambda: check_answer(questions.answers_shuffled[3]))


questions = Questions()
questions.fetch_questions()
questions.initialize_question()
trivia = questions.trivia
answers = questions.answers_shuffled

window = tk.Tk()
window.title('Trivia')
window.config(pady=PADY * 4, padx=PADY * 4)
window.geometry('600x600')

highest_score = tk.Label(
    text=f'Highest score: {questions.highest_score} from {questions.highest_score_questions} questions')
highest_score.pack(side='top', anchor='center', pady=PADY)

score = tk.Label(text='Score: 0 from 0 questions')
score.pack(side='top', anchor='center', pady=PADY)

question = tk.Label(text=trivia, wraplength=WRAP_LEN, height=5)
question.pack(side='top', anchor='center', pady=PADY)
question.pack_propagate(False)

answer_1_button = tk.Button(text=answers[0], wraplength=WRAP_LEN, command=lambda: check_answer(answers[0]))
answer_1_button.pack(side='top', anchor='center', pady=PADY)

answer_2_button = tk.Button(text=answers[1], wraplength=WRAP_LEN, command=lambda: check_answer(answers[1]))
answer_2_button.pack(side='top', anchor='center', pady=PADY)

answer_3_button = tk.Button(text=answers[2], wraplength=WRAP_LEN, command=lambda: check_answer(answers[2]))
answer_3_button.pack(side='top', anchor='center', pady=PADY)

answer_4_button = tk.Button(text=answers[3], wraplength=WRAP_LEN, command=lambda: check_answer(answers[3]))
answer_4_button.pack(side='top', anchor='center', pady=PADY)

correct_incorrect = tk.Label(text='')
correct_incorrect.pack(side='top', anchor='center', pady=PADY)

previous_answer = tk.Label(text='', wraplength=WRAP_LEN)
previous_answer.pack(side='top', anchor='center', pady=PADY)

window.mainloop()
