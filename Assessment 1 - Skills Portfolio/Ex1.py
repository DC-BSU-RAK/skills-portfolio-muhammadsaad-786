import tkinter as tk
from tkinter import messagebox 
import random # for generating random numbers and operations

# This class will hold all logic and UI for math quiz game.
class MathQuizApp:
    def __init__(self, master):
        # 'master' is the main window of Tkinter application.
        self.master = master
        self.master.title("Arithmetic Quiz Challenge") # Set the window title
        self.master.geometry("600x450") # Giving window a fixed size
        self.master.resizable(False, False) # Preventing user from resizing the window

        # Game State Variables
        # These variables keep track of the current game's progress and settings
        self.score = 0 # Player's current score
        self.current_question_num = 0 # Which question number we are on
        self.total_questions = 10 # Each quiz will have 10 questions
        self.current_answer = None # The correct answer for the current question
        self.attempts_left = 2 # How many tries the player has for the current question
        self.difficulty_level = None # Stores the chosen difficulty
        self.min_val = 0 # Minimum value for numbers in questions depending on difficulty
        self.max_val = 0 # Maximum value for numbers in questions 

        # UI Setup
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0") # Light gray background
        self.main_frame.pack(expand=True, fill="both") # Make it fill the entire window

        # Start the application by showing the difficulty selection menu
        self.display_menu()

    # Helper Function to Clear Screen
    def _clear_frame(self, frame):
    
        for widget in frame.winfo_children():
            widget.destroy() # Destroy each widget to clear the screen


    def display_menu(self): # Displaying the initial menu where the user can select a difficulty level

        self._clear_frame(self.main_frame) # Clear any previous content in the main frame

        # Title for the menu screen
        title_label = tk.Label(
            self.main_frame,
            text="Select Difficulty Level",
            font=('Arial', 24, 'bold'),
            bg="#f0f0f0",
            fg="#333333" # Dark gray text
        )
        title_label.pack(pady=40) # Adding padding above & below

        difficulties = [ # Defining the difficulty options with their display text, internal level name, and a color
            ("1. Easy", "Easy", "#4CAF50"),     # Green for Easy
            ("2. Moderate", "Moderate", "#FFC107"), # Amber for Moderate
            ("3. Advanced", "Advanced", "#F44336")  # Red for Advanced
        ]

        # Creating a button for each difficulty level.
        for text, level, color in difficulties:
            button = tk.Button(
                self.main_frame,
                text=text,
                # Use a lambda function to pass the 'level' argument to our handler.
                command=lambda l=level: self._set_difficulty_and_start_quiz(l),
                font=('Arial', 16),
                bg=color,
                fg="white", # White text on colored buttons
                padx=20,
                pady=10,
                relief="raised", # Giving a 3D button effect
                width=15 # Making all buttons the same width
            )
            button.pack(pady=10) # Packing each button with some vertical padding

    def _set_difficulty_and_start_quiz(self, level): # Setting the number range for questions based on the chosen level and starting the quiz

        self.difficulty_level = level # Store the chosen level

        # Set min and max values for numbers based on difficulty.
        if level == "Easy":
            self.min_val = 1
            self.max_val = 9 # Single-digit numbers
        elif level == "Moderate":
            self.min_val = 10
            self.max_val = 99 # Double-digit numbers
        elif level == "Advanced":
            self.min_val = 1000
            self.max_val = 9999 # Four-digit numbers
        
        # Begin the quiz after selecting difficulty
        self.start_quiz()

    def start_quiz(self): # Preparing the quiz environment and displays the first question.

        self._clear_frame(self.main_frame) # Clear the menu screen

        # Reset game state for a new quiz.
        self.score = 0
        self.current_question_num = 0
        self.attempts_left = 2 # Player gets 2 attempts per question

        # Create a dedicated frame for the quiz questions and input
        self.quiz_frame = tk.Frame(self.main_frame, bg="#e0e0e0", padx=20, pady=20)
        self.quiz_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Label to display the actual math question
        self.question_label = tk.Label(
            self.quiz_frame,
            text="Question will appear here", # Placeholder text
            font=('Arial', 20, 'bold'),
            bg="#e0e0e0",
            wraplength=500 # Making sure long questions wrap to the next line
        )
        self.question_label.pack(pady=25)

        # Entry widget for the user to type their answer
        self.answer_entry = tk.Entry(
            self.quiz_frame,
            font=('Arial', 18),
            width=15,
            justify="center" # Center the text in the entry box
        )
        self.answer_entry.pack(pady=15)
        # Bind the Enter key to the check_answer function for quick input
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        # Button to submit the answer.
        submit_button = tk.Button(
            self.quiz_frame,
            text="Submit Answer",
            command=self.check_answer, # Call check_answer when button is clicked
            font=('Arial', 16),
            bg="#2196F3", # Blue button
            fg="white",
            padx=15,
            pady=8,
            relief="raised"
        )
        submit_button.pack(pady=10)

        # Label to give feedback
        self.feedback_label = tk.Label(
            self.quiz_frame,
            text="", # Starts empty
            font=('Arial', 14, 'italic'),
            bg="#e0e0e0",
            height=2 # Give it some fixed height to prevent layout jumps
        )
        self.feedback_label.pack(pady=10)

        # Label to display the current score and question number.
        self.score_display_label = tk.Label(
            self.quiz_frame,
            text=f"Score: {self.score} | Q: {self.current_question_num}/{self.total_questions}",
            font=('Arial', 14),
            bg="#e0e0e0",
            anchor="e" # Align text to the right
        )
        self.score_display_label.pack(side="bottom", fill="x", pady=10)

        # Now that the UI is set up, generate the first question.
        self.generate_question()

    def randomInt(self): # Generates a random integer within the range defined by the chosen difficulty
        return random.randint(self.min_val, self.max_val)

    def decideOperation(self): # Randomly picks either addition or subtraction for the problem
        return random.choice(['+', '-'])

    def generate_question(self): # Creates a new math problem, updates the question label, and prepares for user input. If all questions are done, it calls the results screen.
        if self.current_question_num >= self.total_questions: # Check if we've gone through all the questions
            self.show_results() # If so, show the final results.
            return

        self.current_question_num += 1 # Move to the next question
        self.attempts_left = 2 # Reset attempts for this new question

        # Get two random numbers based on the difficulty.
        num1 = self.randomInt()
        num2 = self.randomInt()
        operator = self.decideOperation() # Get a random operation

        # For subtraction, ensure the first number is larger or equal to avoid negative results
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1 # Swap them to ensure a positive or zero result

        # Constructing the question string
        question_text = f"Question {self.current_question_num}/{self.total_questions}: What is {num1} {operator} {num2}?"
        self.question_label.config(text=question_text) # Update the question label

        # Calculate the correct answer
        if operator == '+':
            self.current_answer = num1 + num2
        else: 
            self.current_answer = num1 - num2

        # Clear the previous answer from the entry box and any feedback
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.answer_entry.focus_set() # Put the cursor back in the entry box

        # Update the score and question count display.
        self.score_display_label.config(text=f"Score: {self.score} | Q: {self.current_question_num}/{self.total_questions}")

    def check_answer(self): # Check the user's input against the correct answer, update the score, and provide feedback.
        try:
            user_answer = int(self.answer_entry.get()) # Try to convert user input to an integer

            if user_answer == self.current_answer:
                # Correct answer! Award points based on attempt.
                if self.attempts_left == 2:
                    self.score += 10 # 10 points for first attempt
                    self.feedback_label.config(text="Correct! (+10 points)", fg="green")
                elif self.attempts_left == 1:
                    self.score += 5 # 5 points for second attempt
                    self.feedback_label.config(text="Correct! (+5 points on second attempt)", fg="green")
                
                # Update the score display immediately
                self.score_display_label.config(text=f"Score: {self.score} | Q: {self.current_question_num}/{self.total_questions}")
                # Waiting a bit then move to the next question
                self.master.after(1500, self.generate_question) # 1.5 second delay
            else:
                # Incorrect answer.
                self.attempts_left -= 1 # Decrement attempts

                if self.attempts_left == 1:
                    # Still one attempt left.
                    self.feedback_label.config(text="Incorrect. Try again!", fg="red")
                    self.answer_entry.delete(0, tk.END) # Clear the wrong answer
                    self.answer_entry.focus_set() # Let them try again
                else: # attempts_left == 0, no more tries for this question
                    self.feedback_label.config(text=f"Incorrect. The answer was {self.current_answer}.", fg="red")
                    # Wait a bit, then move to the next question (no points for this one).
                    self.master.after(2000, self.generate_question) # 2 second delay
        except ValueError:
            # If the user didn't enter a valid number.
            self.feedback_label.config(text="Please enter a valid number.", fg="orange")
            self.answer_entry.focus_set() # Keep focus on the entry box

    # --- Results Screen Functions ---
    def show_results(self): # Displays the final score, calculates a rank, and offers to play again
        self._clear_frame(self.main_frame) # Clear the quiz screen

        # Calculate the maximum possible score (10 questions * 10 points each).
        max_possible_score = self.total_questions * 10
        # Calculate the percentage score.
        percentage = (self.score / max_possible_score) * 100 if max_possible_score > 0 else 0
        
        # Determine the rank based on the percentage.
        rank = "F" # Default rank
        if percentage >= 90:
            rank = "A+"
        elif percentage >= 80:
            rank = "A"
        elif percentage >= 70:
            rank = "B"
        elif percentage >= 60:
            rank = "C"
        elif percentage >= 50:
            rank = "D"

        # Display "Quiz Finished!" title.
        results_label = tk.Label(
            self.main_frame,
            text="Quiz Finished!",
            font=('Arial', 28, 'bold'),
            bg="#f0f0f0",
            fg="#333333"
        )
        results_label.pack(pady=30)

        # Display the final score and percentage.
        final_score_label = tk.Label(
            self.main_frame,
            text=f"Your final score: {self.score} out of {max_possible_score} ({percentage:.1f}%)",
            font=('Arial', 20),
            bg="#f0f0f0",
            fg="#0066cc" # Blue text
        )
        final_score_label.pack(pady=15)

        # Display the calculated rank.
        rank_label = tk.Label(
            self.main_frame,
            text=f"Your Rank: {rank}",
            font=('Arial', 22, 'bold'),
            bg="#f0f0f0",
            # Use a different color for top ranks.
            fg="#e91e63" if rank in ["A+", "A"] else "#ff9800" # Pink for A/A+, Orange otherwise
        )
        rank_label.pack(pady=15)

        # Button to play the quiz again (goes back to difficulty selection).
        play_again_button = tk.Button(
            self.main_frame,
            text="Play Again",
            command=self.display_menu, # This will reset everything and show the menu
            font=('Arial', 16),
            bg="#607D8B", # Gray-blue button
            fg="white",
            padx=20,
            pady=10,
            relief="raised"
        )
        play_again_button.pack(pady=25)

        # Button to exit the application.
        exit_button = tk.Button(
            self.main_frame,
            text="Exit",
            command=self.master.quit, # Closes the Tkinter window
            font=('Arial', 16),
            bg="#f44336", # Red button
            fg="white",
            padx=20,
            pady=10,
            relief="raised"
        )
        exit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()