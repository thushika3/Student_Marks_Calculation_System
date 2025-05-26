# 🎓 Student Marks Calculation System

## 1. ✅ Project Content

The Student Marks Calculation System is a web-based application that streamlines the process of entering, calculating, and displaying student academic performance. Faculty can log in to record internal (3 mid exams) and external marks, while students can view their calculated grades and final report card.It is tailored for use in schools, colleges, or universities and supports both faculty and student roles.

## 2. 💻 Project Code

The project consists of the following main components:

- `index.html`: Home page with login/registration
- `student-dashboard.html`: Student dashboard with options to view marks and report
- `faculty-dashboard.html`: Faculty dashboard for entering marks
- `report-card.html`: Displays final marks and grades
- `database.js`: Handles database schema and queries

## 3. 🔧 Key Technologies

- **Frontend**: HTML, CSS, JavaScript
- **Backend**:  Python Flask
- **Database**:  MySQL
- **APIs**: RESTful endpoints for student/faculty actions
- **Session Management**: localStorage for storing logged-in user info

## 4. 📝 Description

This system allows:

- Faculty to log in and submit internal marks (Mid1, Mid2, Mid3) and external marks.
- Internal marks are calculated by selecting the best 2 midterm scores and averaging them.(25 each)
- Final marks are computed by summing internal average and external marks. (externals = 75 marks)
- Grades are assigned based on final marks.
- Students can log in to view:
  - Subject-wise breakdown of internal, external, and final marks
  - Assigned grade per subject
  - Overall total and average marks
-Faculty can log in to view:
  - Insertion of internas and externals
  - View all student's externals
  - View all there students

## 5. 📊 Output
# Homepage --
![Screenshot 2025-05-26 210022](https://github.com/user-attachments/assets/0632301e-d1aa-49e5-a0b2-5673b3ac5e1c)

# Faculty Dashboard --
![Screenshot 2025-05-26 210310](https://github.com/user-attachments/assets/ef5e9a60-0e4c-4bc4-b44e-157534ed20ce)

# Student Dashboard --
![Screenshot 2025-05-26 210219](https://github.com/user-attachments/assets/37cb414f-f76d-4370-b1af-3bc2c2a5c3c3)

# Insertion of internal marks -- 
![Screenshot 2025-05-26 210433](https://github.com/user-attachments/assets/01c1a720-2f1c-4301-9652-e4c074001e64)

# Final Report Card --
![Screenshot 2025-05-26 210727](https://github.com/user-attachments/assets/08171607-7d3e-46db-be76-e9b0779ed51f)


## 6. 🔍 Further Research

- Implement PDF export for report cards
- Add authentication using JWT instead of localStorage
- Include charts and analytics for progress tracking
- Develop mobile-responsive UI
- Add student feedback system for each subject

