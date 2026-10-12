
# Login and To-Do List Web Application

## 1. Team Members and Contributions

- Name: [salma hady abdelaziz]
- Student ID: [2304046]



## 2. Technologies Used

### Back End
- Python
- Flask
- bcrypt for password hashing
- python-dotenv for environment configuration

### Front End
- HTML for page structure
- CSS for styling and responsive layout
- JavaScript for client-side validation

### Database
- MySQL
- mysql-connector-python for connecting Python to MySQL

### Version Control
- Git and GitHub

## 3. How to Run the Project from an Empty Machine

### Prerequisites
Install:
- Python
- MySQL Server
- MySQL Workbench
- Git 

### Step 1: Obtain the Project
Clone the repository from GitHub or download the project files.

### Step 2: Open the Project Folder
Open the project folder in VS Code and open a terminal in that folder.

### Step 3: Create and Activate a Virtual Environment
Run:

    python -m venv .venv

On Windows PowerShell, activate it using:

    .venv\Scripts\Activate.ps1

### Step 4: Install Dependencies
Run:

    python -m pip install Flask mysql-connector-python bcrypt python-dotenv

### Step 5: Create the Database
Open MySQL Workbench, connect to the MySQL server, open
database/schema.sql, and execute the script.

This creates the registration database and its users and todos tables.

### Step 6: Configure Environment Variables
Copy .env.example to a new file named .env.

On Windows PowerShell, you can use:

    Copy-Item .env.example .env

Edit .env and enter the correct local MySQL settings.
Set SECRET_KEY to a long, random secret value.

Do not commit or upload the real .env file.

### Step 7: Start the Server
In the activated virtual environment, run:

    python app.py

### Step 8: Open the Application
Open this address in your browser:

    http://127.0.0.1:5000

## 4. Implemented Features (R1–R10)

Map each requirement below to the exact R-number and wording in the assignment.

- [R1: Registration — describe the implemented behavior]
- [R2: Login — describe the implemented behavior]
- [R3: Password hashing using bcrypt]
- [R4: Session-based authentication]
- [R5: Add a to-do]
- [R6: List the current user's to-dos]
- [R7: Mark a to-do as done or not done]
- [R8: Edit a to-do]
- [R9: Delete a to-do]
- [R10: Validation and user-specific data protection]
- [R11: dark ,mode]


Additional implemented details:
- Client-side and server-side input validation
- Parameterized SQL queries
- Database foreign key constraint
- Responsive layout for phone-sized screens

Bonus features:
- [dark mode.]




   ## 5. Screenshots

All required screenshots are included in the screenshots folder.

## 6. Answers to the Assignment Questions

### (a) Why do UPDATE and DELETE contain AND user_id = ?, and what changes if it is removed?

The user ID condition ensures that the operation affects only a task
belonging to the currently logged-in user. Without this condition,
a user might modify or delete another user's task by supplying or
guessing its task ID. Checking ownership helps enforce authorization.

### (b) What happens if a to-do is inserted for a user_id that does not exist, and which constraint is this?

The database rejects the insertion because the user_id in the todos
table references the users table. This is the foreign key constraint,
which enforces referential integrity.

### (c) Why store a hash instead of the password?

A password hash avoids storing the original password in readable form.
The application stores a bcrypt hash and verifies login attempts using
bcrypt.checkpw(). bcrypt uses a salt and is designed for password hashing.

### (d) The name column is NOT NULL. Why is an additional empty-name check needed?

NOT NULL prevents SQL NULL values, but an empty string is still a
valid string value. The application must validate that the name is
not empty or only whitespace before inserting it into the database.
