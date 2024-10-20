import tkinter as tk
from tkinter import messagebox, scrolledtext

# This class models a student's data, encapsulating all relevant attributes and methods.
class Student:
    def __init__(self, student_number, name, coursework_marks, exam_mark):
        # Initializing the student object with their details
        self.student_number = student_number  # Unique student ID
        self.name = name  # Student's full name
        self.coursework_marks = coursework_marks  # List of marks for coursework assignments
        self.exam_mark = exam_mark  # The student's exam mark

        # Calculate the total marks from coursework
        self.total_coursework = sum(coursework_marks)  
        # Add the coursework and exam marks to get the overall total score
        self.total_marks = self.total_coursework + exam_mark  
        # Calculate the student's percentage based on a total possible score of 160
        self.percentage = (self.total_marks / 160) * 100  
        # Determine the student's grade based on their percentage
        self.grade = self.calculate_grade()

    # Method to calculate the grade from the student's percentage
    def calculate_grade(self):
        # Basic grade boundaries: A for 70%+, B for 60-69%, etc.
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'  # If the percentage is below 40%, it's a fail

    # Method to return the student's details in a readable format
    def display(self):
        return (f"{self.name} ({self.student_number})\n"
                f"Total coursework marks: {self.total_coursework}/60\n"
                f"Exam mark: {self.exam_mark}/100\n"
                f"Overall percentage: {self.percentage:.2f}%\n"
                f"Grade: {self.grade}\n\n")

# Function to load student data from a file
def load_student_data(filename):
    students = []  # Create an empty list to store the student objects
    with open(filename, 'r') as file:
        num_students = int(file.readline().strip())  # Read the number of students from the file
        for line in file:
            # Split the line into its different parts: student number, name, coursework marks, and exam mark
            parts = line.strip().split(',')
            student_number = int(parts[0])  # First part is the student number
            name = parts[1]  # Second part is the student's name
            coursework_marks = list(map(int, parts[2:5]))  # Next three parts are the coursework marks
            exam_mark = int(parts[5])  # Last part is the exam mark

            # Create a Student object and add it to the list
            students.append(Student(student_number, name, coursework_marks, exam_mark))

    # Return the list of students
    return students

# Main application class for the Student Record System
class StudentApp:
    def __init__(self, root):
        # Setting up the main window
        self.root = root
        self.root.title("Student Record System")  # Title of the app window
        self.root.geometry('600x500')  # Dimensions of the window
        self.root.config(bg="#f5f5f5")  # Set a light background color

        # Load student data from a file (hardcoded file name here)
        self.students = load_student_data('studentMarks.txt')

        # Call the function to set up the layout (buttons, text box, etc.)
        self.create_layout()

    def create_layout(self):
        # Title label at the top of the window
        self.title_label = tk.Label(self.root, text="Student Record System", font=("Helvetica", 20), bg="#f5f5f5")
        self.title_label.pack(pady=20)  # Add some vertical padding

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.button_frame.pack(pady=10)

        # Button to view all student records
        self.view_all_button = tk.Button(self.button_frame, text="View All Student Records", command=self.view_all_students, width=25, height=2)
        self.view_all_button.grid(row=0, column=0, padx=10, pady=5)

        # Button to view a single student's record
        self.view_individual_button = tk.Button(self.button_frame, text="View Individual Student Record", command=self.view_individual_student, width=25, height=2)
        self.view_individual_button.grid(row=0, column=1, padx=10, pady=5)

        # Button to find and display the student with the highest score
        self.highest_score_button = tk.Button(self.button_frame, text="Show Highest Scoring Student", command=self.show_highest_score_student, width=25, height=2)
        self.highest_score_button.grid(row=1, column=0, padx=10, pady=5)

        # Button to find and display the student with the lowest score
        self.lowest_score_button = tk.Button(self.button_frame, text="Show Lowest Scoring Student", command=self.show_lowest_score_student, width=25, height=2)
        self.lowest_score_button.grid(row=1, column=1, padx=10, pady=5)

        # Scrolled text box for displaying the student records or messages
        self.text_box = scrolledtext.ScrolledText(self.root, width=70, height=15, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_box.pack(pady=10)

    # Function to display all student records
    def view_all_students(self):
        self.text_box.delete(1.0, tk.END)  # Clear the text box
        total_percentage = 0  # Initialize a variable to track the total percentage
        result = ""  # String to accumulate the results

        # Loop through each student and collect their display information
        for student in self.students:
            result += student.display()  # Add each student's data to the result string
            total_percentage += student.percentage  # Add their percentage to the total

        # Calculate the average percentage of all students
        average_percentage = total_percentage / len(self.students)
        result += f"Total students: {len(self.students)}\n"  # Add the number of students to the result
        result += f"Average percentage: {average_percentage:.2f}%\n"  # Add the average percentage to the result

        # Display all the accumulated data in the text box
        self.text_box.insert(tk.END, result)

    # Function to open a new window for selecting a student to view their record
    def view_individual_student(self):
        self.select_window = tk.Toplevel(self.root)  # Create a new window
        self.select_window.title("Select Student")  # Title of the new window
        self.select_window.geometry('300x400')  # Dimensions of the new window

        # Listbox for selecting a student by name
        self.student_listbox = tk.Listbox(self.select_window, font=("Helvetica", 12))
        for student in self.students:
            self.student_listbox.insert(tk.END, student.name)  # Add each student's name to the listbox
        self.student_listbox.pack(pady=20)

        # Button to confirm the selected student
        self.select_button = tk.Button(self.select_window, text="View Record", command=self.show_individual_record)
        self.select_button.pack(pady=10)

    # Function to show the selected student's record
    def show_individual_record(self):
        selected_index = self.student_listbox.curselection()  # Get the index of the selected student
        if selected_index:  # Ensure a student is selected
            student = self.students[selected_index[0]]  # Retrieve the student object
            self.text_box.delete(1.0, tk.END)  # Clear the text box
            self.text_box.insert(tk.END, student.display())  # Show the student's data in the text box

    # Function to find and display the highest scoring student
    def show_highest_score_student(self):
        highest_student = max(self.students, key=lambda s: s.total_marks)  # Find the student with the highest total marks
        self.text_box.delete(1.0, tk.END)  # Clear the text box
        self.text_box.insert(tk.END, highest_student.display())  # Display their record

    # Function to find and display the lowest scoring student
    def show_lowest_score_student(self):
        lowest_student = min(self.students, key=lambda s: s.total_marks)  # Find the student with the lowest total marks
        self.text_box.delete(1.0, tk.END)  # Clear the text box
        self.text_box.insert(tk.END, lowest_student.display())  # Display their record

# Entry point for the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = StudentApp(root)  # Instantiate the StudentApp
    root.mainloop()  # Run the Tkinter event loop
