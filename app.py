from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "name": "Tricia Aguilar", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Cruz", "grade": 11, "section": "Genesis"}
]

@app.route('/')
def home():
    # must return the HTML file
    return render_template('index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
