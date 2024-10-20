import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

# Define a class to represent each student and their details
class Student:
    def __init__(self, student_number, name, coursework_marks, exam_mark):
        # Initialize student attributes
        self.student_number = student_number  # Unique identifier for the student
        self.name = name  # Name of the student
        self.coursework_marks = coursework_marks  # List of coursework marks
        self.exam_mark = exam_mark  # Exam mark received

        # Calculate total coursework marks and overall total marks
        self.total_coursework = sum(coursework_marks)  # Sum up the coursework marks
        self.total_marks = self.total_coursework + exam_mark  # Calculate overall marks (coursework + exam)
        self.percentage = (self.total_marks / 160) * 100  # Calculate percentage out of 100
        self.grade = self.calculate_grade()  # Determine the grade based on the percentage

    # Method to determine the student's grade based on their percentage
    def calculate_grade(self):
        # Use a simple grading scale to assign grades
        if self.percentage >= 70:
            return 'A'  # Excellent performance
        elif self.percentage >= 60:
            return 'B'  # Good performance
        elif self.percentage >= 50:
            return 'C'  # Average performance
        elif self.percentage >= 40:
            return 'D'  # Below average performance
        else:
            return 'F'  # Failed

    # Method to format student details for display purposes
    def display(self):
        return (f"Student: {self.name} ({self.student_number})\n"
                f"Total Coursework Marks: {self.total_coursework}/60\n"
                f"Exam Mark: {self.exam_mark}/100\n"
                f"Overall Percentage: {self.percentage:.2f}%\n"
                f"Grade: {self.grade}\n\n")  # Display all important info in a readable format


# Function to load student data from a specified file
def load_student_data(filename):
    students = []  # Create an empty list to store student instances
    try:
        with open(filename, 'r') as file:
            # First line should contain the number of students
            num_students = int(file.readline().strip())  # Read the first line for the count
            # Process each subsequent line to read student records
            for line in file:
                parts = line.strip().split(',')  # Split the line into parts
                student_number = int(parts[0])  # First part: student number
                name = parts[1]  # Second part: student's name
                coursework_marks = list(map(int, parts[2:5]))  # Next three parts: coursework marks
                exam_mark = int(parts[5])  # Last part: exam mark

                # Create a new Student object and append it to the list
                students.append(Student(student_number, name, coursework_marks, exam_mark))
    except FileNotFoundError:
        # Handle the case where the specified file does not exist
        messagebox.showerror("Error", f"File {filename} not found!")  # Notify the user of the error
    except Exception as e:
        # Catch any other exceptions and show an error message
        messagebox.showerror("Error", f"An error occurred while loading student data: {e}")
    
    return students  # Return the list of students loaded from the file


# Main application class for the student records system
class StudentApp:
    def __init__(self, root):
        # Initialize the main application window and its properties
        self.root = root  # Main window
        self.root.title("Student Record System")  # Set the window title
        self.root.geometry('700x600')  # Define the size of the window
        self.root.config(bg="#f5f5f5")  # Set a light background color for the window

        # Load student data from the text file into the application
        self.students = load_student_data('studentMarks.txt')

        # Track the windows and widgets that will be used in the app
        self.select_window = None  # For selecting individual students
        self.student_listbox = None  # Listbox for displaying students
        self.select_button = None  # Button for selecting a student

        # Set up the layout of the application interface
        self.create_layout()

    # Method to create the main layout of the application
    def create_layout(self):
        # Create and pack a title label at the top of the window
        self.title_label = tk.Label(self.root, text="Student Record System", font=("Helvetica", 20), bg="#f5f5f5")
        self.title_label.pack(pady=20)  # Add some vertical padding

        # Create a frame to hold buttons for various operations
        self.button_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.button_frame.pack(pady=10)  # Add some vertical padding

        # Add buttons for different functionalities (viewing, adding, sorting, etc.)
        self.view_all_button = tk.Button(self.button_frame, text="View All Student Records", command=self.view_all_students, width=25, height=2)
        self.view_all_button.grid(row=0, column=0, padx=10, pady=5)  # Arrange buttons in a grid

        self.view_individual_button = tk.Button(self.button_frame, text="View Individual Student Record", command=self.view_individual_student, width=25, height=2)
        self.view_individual_button.grid(row=0, column=1, padx=10, pady=5)

        self.sort_button = tk.Button(self.button_frame, text="Sort Records", command=self.sort_records, width=25, height=2)
        self.sort_button.grid(row=1, column=0, padx=10, pady=5)

        self.add_button = tk.Button(self.button_frame, text="Add Student", command=self.add_student, width=25, height=2)
        self.add_button.grid(row=1, column=1, padx=10, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Student", command=self.delete_student, width=25, height=2)
        self.delete_button.grid(row=2, column=0, padx=10, pady=5)

        self.update_button = tk.Button(self.button_frame, text="Update Student", command=self.update_student, width=25, height=2)
        self.update_button.grid(row=2, column=1, padx=10, pady=5)

        # Create a scrollable text box to display student records
        self.text_box = scrolledtext.ScrolledText(self.root, width=80, height=20, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_box.pack(pady=10)  # Add padding for aesthetics

    # Function to display all student records in the text box
    def view_all_students(self):
        self.text_box.delete(1.0, tk.END)  # Clear the text box to prepare for new content
        total_percentage = 0  # Initialize total percentage for calculating the average
        result = ""  # Prepare a result string to accumulate student information

        # Loop through each student and gather their information
        for student in self.students:
            result += student.display()  # Append each student's display information
            total_percentage += student.percentage  # Add this student's percentage to the total

        # Calculate and display the average percentage across all students
        average_percentage = total_percentage / len(self.students) if self.students else 0  # Avoid division by zero
        result += f"Total students: {len(self.students)}\n"
        result += f"Average percentage: {average_percentage:.2f}%\n"
        self.text_box.insert(tk.END, result)  # Insert the result into the text box

    # Function to sort student records based on user-defined criteria
    def sort_records(self):
        sort_choice = simpledialog.askstring("Sort Records", "Enter sort criteria (name, marks, grade):")  # Ask user for sort criteria

        # Sort the student list based on the criteria provided
        if sort_choice == "name":
            self.students.sort(key=lambda s: s.name)  # Sort alphabetically by name
        elif sort_choice == "marks":
            self.students.sort(key=lambda s: s.total_marks, reverse=True)  # Sort by total marks (highest first)
        elif sort_choice == "grade":
            self.students.sort(key=lambda s: s.grade)  # Sort by grade
        else:
            # Show error if the criteria entered is invalid
            messagebox.showerror("Error", "Invalid sort criteria")
            return

        # Refresh the display after sorting
        self.view_all_students()

    # Function to add a new student record
    def add_student(self):
        try:
            # Prompt user for student details
            student_number = int(simpledialog.askstring("Input", "Enter student number:"))  # Get student number
            name = simpledialog.askstring("Input", "Enter student name:")  # Get student's name
            coursework_marks = [
                int(simpledialog.askstring("Input", f"Enter coursework mark {i+1}:"))  # Get each coursework mark
                for i in range(3)
            ]
            exam_mark = int(simpledialog.askstring("Input", "Enter exam mark:"))  # Get exam mark

            # Create a new Student object and add it to the list
            new_student = Student(student_number, name, coursework_marks, exam_mark)
            self.students.append(new_student)  # Append the new student to the list
            messagebox.showinfo("Success", "Student record added successfully!")  # Notify the user of success
            self.view_all_students()  # Refresh the display to show the new student
        except ValueError:
            # Handle any invalid input
            messagebox.showerror("Error", "Invalid input, please try again.")

    # Function to delete an existing student record
    def delete_student(self):
        self.view_individual_student()  # Open the selection window to choose a student
        if self.student_listbox is not None:  # Check if the listbox is ready
            self.select_button.config(command=self.confirm_delete_student)  # Set the button command to confirm deletion

    # Function to confirm the deletion of a selected student
    def confirm_delete_student(self):
        selected_index = self.student_listbox.curselection()  # Get the index of the selected student
        if selected_index:
            student = self.students[selected_index[0]]  # Retrieve the selected student
            # Ask for confirmation before deleting the record
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student.name}'s record?"):
                del self.students[selected_index[0]]  # Remove the student from the list
                self.select_window.destroy()  # Close the selection window
                messagebox.showinfo("Success", "Student record deleted.")  # Notify the user
                self.view_all_students()  # Refresh the student records display

    # Function to update a student's record
    def update_student(self):
        self.view_individual_student()  # Open the selection window to choose a student
        if self.student_listbox is not None:
            self.select_button.config(command=self.confirm_update_student)  # Set the button to confirm the update

    # Function to confirm and update the selected student's record
    def confirm_update_student(self):
        selected_index = self.student_listbox.curselection()  # Get the index of the selected student
        if selected_index:
            student = self.students[selected_index[0]]  # Retrieve the selected student

            try:
                # Prompt the user to input updated details for the selected student
                student.name = simpledialog.askstring("Input", f"Enter new name for {student.name}:")  # Update name
                student.coursework_marks = [
                    int(simpledialog.askstring("Input", f"Enter new coursework mark {i+1} for {student.name}:"))  # Update each coursework mark
                    for i in range(3)
                ]
                student.exam_mark = int(simpledialog.askstring("Input", f"Enter new exam mark for {student.name}:"))  # Update exam mark

                # Recalculate the student's total marks, percentage, and grade
                student.total_coursework = sum(student.coursework_marks)  # Update coursework total
                student.total_marks = student.total_coursework + student.exam_mark  # Update overall total marks
                student.percentage = (student.total_marks / 160) * 100  # Recalculate percentage
                student.grade = student.calculate_grade()  # Recalculate grade

                self.select_window.destroy()  # Close the selection window after updating
                messagebox.showinfo("Success", "Student record updated.")  # Notify the user
                self.view_all_students()  # Refresh the display to show updated records
            except ValueError:
                # Show an error if any input is invalid
                messagebox.showerror("Error", "Invalid input, please try again.")

    # Function to open a window to select a student from a list
    def view_individual_student(self):
        self.select_window = tk.Toplevel(self.root)  # Create a new window for selection
        self.select_window.title("Select Student")  # Set the window title
        self.select_window.geometry('300x400')  # Set the size of the window

        # Create a listbox to display the names of all students
        self.student_listbox = tk.Listbox(self.select_window, font=("Helvetica", 12))  # Configure the listbox appearance
        for student in self.students:
            self.student_listbox.insert(tk.END, student.name)  # Add each student's name to the listbox
        self.student_listbox.pack(pady=20)  # Pack the listbox with some padding

        # Add a button to view the selected student's record
        self.select_button = tk.Button(self.select_window, text="View Record", command=self.show_individual_record)  # Set up the button
        self.select_button.pack(pady=10)  # Add padding for aesthetics

    # Function to display the selected student's record
    def show_individual_record(self):
        selected_index = self.student_listbox.curselection()  # Get the index of the selected student
        if selected_index:
            student = self.students[selected_index[0]]  # Retrieve the selected student
            self.text_box.delete(1.0, tk.END)  # Clear the text box
            self.text_box.insert(tk.END, student.display())  # Insert the student's details into the text box


# Entry point for running the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = StudentApp(root)  # Initialize the StudentApp with the root window
    root.mainloop()  # Start the Tkinter event loop
