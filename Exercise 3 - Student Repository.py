import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

# Student class to hold student details and perform calculations
class Student:
    def __init__(self, student_number, name, coursework_marks, exam_mark):
        self.student_number = student_number
        self.name = name
        self.coursework_marks = coursework_marks
        self.exam_mark = exam_mark

        self.total_coursework = sum(coursework_marks)  # Total coursework marks out of 60
        self.total_marks = self.total_coursework + exam_mark  # Total marks (coursework + exam) out of 160
        self.percentage = (self.total_marks / 160) * 100  # Percentage based on total marks
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

    def display(self):
        return (f"Student: {self.name} ({self.student_number})\n"
                f"Total Coursework Marks: {self.total_coursework}/60\n"
                f"Exam Mark: {self.exam_mark}/100\n"
                f"Overall Percentage: {self.percentage:.2f}%\n"
                f"Grade: {self.grade}\n\n")


# Function to load student data from a file
def load_student_data(filename):
    students = []
    try:
        with open(filename, 'r') as file:
            num_students = int(file.readline().strip())  # Read number of students
            for line in file:
                parts = line.strip().split(',')
                student_number = int(parts[0])
                name = parts[1]
                coursework_marks = list(map(int, parts[2:5]))  # Coursework marks
                exam_mark = int(parts[5])  # Exam mark

                students.append(Student(student_number, name, coursework_marks, exam_mark))
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {filename} not found!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading student data: {e}")
    
    return students


# Main application class for the Student Record System
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record System")
        self.root.geometry('700x600')
        self.root.config(bg="#f5f5f5")

        self.students = load_student_data('studentMarks.txt')

        # Variables to track additional windows and widgets
        self.select_window = None
        self.student_listbox = None
        self.select_button = None

        # Create the main layout with buttons and text box
        self.create_layout()

    def create_layout(self):
        self.title_label = tk.Label(self.root, text="Student Record System", font=("Helvetica", 20), bg="#f5f5f5")
        self.title_label.pack(pady=20)

        self.button_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.button_frame.pack(pady=10)

        self.view_all_button = tk.Button(self.button_frame, text="View All Student Records", command=self.view_all_students, width=25, height=2)
        self.view_all_button.grid(row=0, column=0, padx=10, pady=5)

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

        self.text_box = scrolledtext.ScrolledText(self.root, width=80, height=20, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_box.pack(pady=10)

    def view_all_students(self):
        self.text_box.delete(1.0, tk.END)
        total_percentage = 0
        result = ""

        for student in self.students:
            result += student.display()
            total_percentage += student.percentage

        average_percentage = total_percentage / len(self.students)
        result += f"Total students: {len(self.students)}\n"
        result += f"Average percentage: {average_percentage:.2f}%\n"
        self.text_box.insert(tk.END, result)

    def sort_records(self):
        sort_choice = simpledialog.askstring("Sort Records", "Enter sort criteria (name, marks, grade):")

        if sort_choice == "name":
            self.students.sort(key=lambda s: s.name)
        elif sort_choice == "marks":
            self.students.sort(key=lambda s: s.total_marks, reverse=True)
        elif sort_choice == "grade":
            self.students.sort(key=lambda s: s.grade)
        else:
            messagebox.showerror("Error", "Invalid sort criteria")
            return

        self.view_all_students()

    def add_student(self):
        try:
            student_number = int(simpledialog.askstring("Input", "Enter student number:"))
            name = simpledialog.askstring("Input", "Enter student name:")
            coursework_marks = [
                int(simpledialog.askstring("Input", f"Enter coursework mark {i+1}:"))
                for i in range(3)
            ]
            exam_mark = int(simpledialog.askstring("Input", "Enter exam mark:"))

            new_student = Student(student_number, name, coursework_marks, exam_mark)
            self.students.append(new_student)
            messagebox.showinfo("Success", "Student record added successfully!")
            self.view_all_students()
        except ValueError:
            messagebox.showerror("Error", "Invalid input, please try again.")

    def delete_student(self):
        self.view_individual_student()  
        if self.student_listbox is not None:
            self.select_button.config(command=self.confirm_delete_student)

    def confirm_delete_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            student = self.students[selected_index[0]]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student.name}'s record?"):
                del self.students[selected_index[0]]
                self.select_window.destroy()
                messagebox.showinfo("Success", "Student record deleted.")
                self.view_all_students()

    def update_student(self):
        self.view_individual_student()  
        if self.student_listbox is not None:
            self.select_button.config(command=self.confirm_update_student)

    def confirm_update_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            student = self.students[selected_index[0]]

            try:
                student.name = simpledialog.askstring("Input", f"Enter new name for {student.name}:")
                student.coursework_marks = [
                    int(simpledialog.askstring("Input", f"Enter new coursework mark {i+1} for {student.name}:"))
                    for i in range(3)
                ]
                student.exam_mark = int(simpledialog.askstring("Input", f"Enter new exam mark for {student.name}:"))

                student.total_coursework = sum(student.coursework_marks)
                student.total_marks = student.total_coursework + student.exam_mark
                student.percentage = (student.total_marks / 160) * 100
                student.grade = student.calculate_grade()

                self.select_window.destroy()
                messagebox.showinfo("Success", "Student record updated.")
                self.view_all_students()
            except ValueError:
                messagebox.showerror("Error", "Invalid input, please try again.")

    def view_individual_student(self):
        self.select_window = tk.Toplevel(self.root)
        self.select_window.title("Select Student")
        self.select_window.geometry('300x400')

        self.student_listbox = tk.Listbox(self.select_window, font=("Helvetica", 12))
        for student in self.students:
            self.student_listbox.insert(tk.END, student.name)
        self.student_listbox.pack(pady=20)

        self.select_button = tk.Button(self.select_window, text="View Record", command=self.show_individual_record)
        self.select_button.pack(pady=10)

    def show_individual_record(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            student = self.students[selected_index[0]]
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, student.display())


# Main loop to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
