from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"  # for flash messages


# ------------------ DATABASE SETUP ------------------
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT,
                    section TEXT
                )''')
    conn.commit()
    conn.close()


# ------------------ ROUTES ------------------
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        section = request.form['section']

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, age, grade, section) VALUES (?, ?, ?, ?)",
                  (name, age, grade, section))
        conn.commit()
        conn.close()
        flash("Student added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add_student.html')


@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "danger")
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        section = request.form['section']
        c.execute("UPDATE students SET name=?, age=?, grade=?, section=? WHERE id=?",
                  (name, age, grade, section, id))
        conn.commit()
        conn.close()
        flash("Student updated successfully!", "info")
        return redirect(url_for('index'))

    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()
    conn.close()
    return render_template('add_student.html', student=student)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
