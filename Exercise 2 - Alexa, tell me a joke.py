import tkinter as tk
import random

# Function to load jokes from a file
def load_jokes(filename):
    jokes = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Loop through lines two by two (setup and punchline)
        for i in range(0, len(lines), 2):
            setup = lines[i].strip()  # Get the setup (remove extra whitespace)
            if i + 1 < len(lines):
                punchline = lines[i + 1].strip()  # Get the punchline
                jokes.append({"setup": setup, "punchline": punchline})
    return jokes

# The User Interface of the tkinter program
class JokeApp:
    def __init__(self, root, jokes):
        self.root = root
        self.root.title("Alexa, Tell Me a Joke")
        self.jokes = jokes

        # The setup label
        self.setup_label = tk.Label(self.root, text="Alexa, tell me a joke!", font=("Arial", 14))
        self.setup_label.pack(pady=10)

        # The punchline label that is empty at the start
        self.punchline_label = tk.Label(self.root, text="", font=("Arial", 14, "italic"))
        self.punchline_label.pack(pady=10)

        # The button to show joke setup
        self.tell_joke_button = tk.Button(self.root, text="Tell me a Joke", font=("Arial", 12), command=self.show_joke)
        self.tell_joke_button.pack(pady=5)

        # The button to reveal the punchline
        self.show_punchline_button = tk.Button(self.root, text="Show Punchline", font=("Arial", 12), command=self.show_punchline)
        self.show_punchline_button.pack(pady=5)

        # The quit button to quit the app
        self.quit_button = tk.Button(self.root, text="Quit", font=("Arial", 12), command=self.root.quit)
        self.quit_button.pack(pady=20)

        # Holds the current joke
        self.current_joke = None

    # Function that selects a random joke
    def show_joke(self):
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke["setup"])
        self.punchline_label.config(text="")  # Clear the previous punchline

    # Function that shows the punchline
    def show_punchline(self):
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke["punchline"])

# Running the application
if __name__ == "__main__":
    # Load jokes from the file
    jokes = load_jokes("randomJokes.txt")

    if not jokes:
        print("No jokes available.")
    else:
        root = tk.Tk()
        app = JokeApp(root, jokes)
        root.mainloop()
