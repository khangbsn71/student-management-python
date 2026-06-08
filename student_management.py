"""
Student Management System
-------------------------
A small console application for managing student records.

Features:
- Add new students
- List all students
- Search by student ID
- Update student scores
- Delete a student
- Calculate average score
- Classify academic performance
- Save data to a JSON file

This project uses only the Python standard library.
"""

import json
from pathlib import Path


DATA_FILE = Path("students.json")


class Student:
    def __init__(self, student_id, full_name, math_score, english_score, programming_score):
        self.student_id = student_id
        self.full_name = full_name
        self.math_score = math_score
        self.english_score = english_score
        self.programming_score = programming_score

    def average_score(self):
        return round((self.math_score + self.english_score + self.programming_score) / 3, 2)

    def classification(self):
        avg = self.average_score()

        if avg >= 8.0:
            return "Excellent"
        if avg >= 6.5:
            return "Good"
        if avg >= 5.0:
            return "Average"
        return "Needs Improvement"

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "math_score": self.math_score,
            "english_score": self.english_score,
            "programming_score": self.programming_score,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"],
            data["full_name"],
            data["math_score"],
            data["english_score"],
            data["programming_score"],
        )


class StudentManager:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        if not DATA_FILE.exists():
            self.students = []
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                self.students = [Student.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            print("Warning: Could not read data file. Starting with an empty list.")
            self.students = []

    def save_data(self):
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump([student.to_dict() for student in self.students], file, indent=4)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def add_student(self):
        print("\nAdd New Student")

        student_id = input("Student ID: ").strip()
        if not student_id:
            print("Student ID cannot be empty.")
            return

        if self.find_student(student_id):
            print("A student with this ID already exists.")
            return

        full_name = input("Full name: ").strip()
        if not full_name:
            print("Full name cannot be empty.")
            return

        math_score = self.get_score("Math score: ")
        english_score = self.get_score("English score: ")
        programming_score = self.get_score("Programming score: ")

        student = Student(student_id, full_name, math_score, english_score, programming_score)
        self.students.append(student)
        self.save_data()

        print("Student added successfully.")

    def list_students(self):
        print("\nStudent List")

        if not self.students:
            print("No students found.")
            return

        print("-" * 86)
        print(f"{'ID':<12}{'Name':<25}{'Math':>8}{'English':>10}{'Python':>10}{'Average':>10}{'Class':>11}")
        print("-" * 86)

        for student in self.students:
            print(
                f"{student.student_id:<12}"
                f"{student.full_name:<25}"
                f"{student.math_score:>8.2f}"
                f"{student.english_score:>10.2f}"
                f"{student.programming_score:>10.2f}"
                f"{student.average_score():>10.2f}"
                f"{student.classification():>11}"
            )

        print("-" * 86)

    def search_student(self):
        student_id = input("\nEnter student ID to search: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        print("\nStudent Information")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.full_name}")
        print(f"Math: {student.math_score}")
        print(f"English: {student.english_score}")
        print(f"Programming: {student.programming_score}")
        print(f"Average: {student.average_score()}")
        print(f"Classification: {student.classification()}")

    def update_student(self):
        student_id = input("\nEnter student ID to update: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        print("Enter new scores.")
        student.math_score = self.get_score("New math score: ")
        student.english_score = self.get_score("New English score: ")
        student.programming_score = self.get_score("New programming score: ")

        self.save_data()
        print("Student updated successfully.")

    def delete_student(self):
        student_id = input("\nEnter student ID to delete: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        self.students.remove(student)
        self.save_data()
        print("Student deleted successfully.")

    @staticmethod
    def get_score(prompt):
        while True:
            try:
                score = float(input(prompt))
                if 0 <= score <= 10:
                    return score
                print("Score must be between 0 and 10.")
            except ValueError:
                print("Please enter a valid number.")

    def show_menu(self):
        while True:
            print("\n===== Student Management System =====")
            print("1. Add student")
            print("2. List students")
            print("3. Search student")
            print("4. Update student scores")
            print("5. Delete student")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.list_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


def main():
    manager = StudentManager()
    manager.show_menu()


if __name__ == "__main__":
    main()
