import tkinter as tk
from tkinter import messagebox
import random

# This function allows the user to select the difficulty of the math quiz.
def generate_question(level):
    # Depending on the selected difficulty level, generate random numbers within different ranges
    if level == 'easy':
        num1 = random.randint(1, 9)  # Single-digit numbers for easy
        num2 = random.randint(1, 9)
    elif level == 'medium':
        num1 = random.randint(10, 99)  # Two-digit numbers for medium
        num2 = random.randint(10, 99)
    elif level == 'hard':
        num1 = random.randint(1000, 9999)  # Four-digit numbers for hard
        num2 = random.randint(1000, 9999)

    # List of possible operations
    operations = ['+', '-', '*', '/']
    # Randomly choose one operation
    operation = random.choice(operations)

    # If the operation is division, ensure num1 is a multiple of num2 to avoid non-integer results
    if operation == '/':
        num1 = num1 * num2

    # Create a string representation of the question and calculate the answer using eval()
    question = f"{num1} {operation} {num2}"
    return question, eval(question)

# The MathQuizApp class handles the quiz logic and GUI
class MathQuizApp:
    def __init__(self, root):
        self.root = root  # The root window of the app
        self.root.title("Math Quiz")  # Set the window title

        self.level = tk.StringVar()  # Holds the selected difficulty level
        self.score = 0  # The current score
        self.num_questions = 10  # Total number of questions in the quiz
        self.current_question = 0  # Current question number
        self.correct_answer = None  # The correct answer for the current question

        # Initialize the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Welcome label at the top of the window
        self.welcome_label = tk.Label(self.root, text="Welcome to the Math Quiz!", font=("Arial", 16))
        self.welcome_label.pack(pady=10)

        # Label and buttons for difficulty level selection
        self.level_label = tk.Label(self.root, text="Select a level:", font=("Arial", 14))
        self.level_label.pack(pady=5)

        # Buttons for selecting Easy, Medium, or Hard difficulty
        self.easy_button = tk.Button(self.root, text="Easy", font=("Arial", 12), command=lambda: self.start_quiz('easy'))
        self.easy_button.pack(pady=5)

        self.medium_button = tk.Button(self.root, text="Medium", font=("Arial", 12), command=lambda: self.start_quiz('medium'))
        self.medium_button.pack(pady=5)

        self.hard_button = tk.Button(self.root, text="Hard", font=("Arial", 12), command=lambda: self.start_quiz('hard'))
        self.hard_button.pack(pady=5)

        # Label for displaying the math question
        self.question_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.question_label.pack(pady=20)

        # Entry box for the user to type their answer
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        # Submit button for answering the question
        self.submit_button = tk.Button(self.root, text="Submit", font=("Arial", 12), command=self.check_answer)
        self.submit_button.pack(pady=10)

        # Label for displaying the score
        self.score_label = tk.Label(self.root, text="Score: 0/0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Label for displaying feedback (correct/incorrect answers)
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 14), fg="green")
        self.feedback_label.pack(pady=10)

    # Start the quiz with the selected difficulty level
    def start_quiz(self, selected_level):
        self.level.set(selected_level)  # Store the selected difficulty level
        self.score = 0  # Reset score to 0
        self.current_question = 0  # Reset current question number to 0
        self.ask_question()  # Ask the first question

    # Ask a new question
    def ask_question(self):
        if self.current_question < self.num_questions:  # Check if there are questions left
            self.current_question += 1  # Increment the current question number
            question, self.correct_answer = generate_question(self.level.get())  # Generate a new question
            self.question_label.config(text=f"Question {self.current_question}: {question}")  # Update question label
            self.feedback_label.config(text="")  # Clear previous feedback
        else:
            self.end_quiz()  # If no more questions, end the quiz

    # Check if the user's answer is correct
    def check_answer(self):
        user_answer = self.answer_entry.get()  # Get the user's answer from the entry box
        try:
            # Compare user's answer with the correct answer
            if float(user_answer) == self.correct_answer:
                self.feedback_label.config(text="Correct!", fg="green")  # Correct answer
                self.score += 1  # Increase the score
            else:
   