from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Student Management API!"

# Example student data
students = [
    {"id": 1, "name": "Tricia Aguilar", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Cruz", "grade": 11, "section": "Genesis"}
]

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# Get one student
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for s in students:
        if s['id'] == id:
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404

# Add a student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = {
        "id": len(students) + 1,
        "name": data.get("name"),
        "grade": data.get("grade"),
        "section": data.get("section")
    }
    students.append(new_student)
    return jsonify({"message": "Student added successfully!", "student": new_student}), 201

# Update a student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    for s in students:
        if s['id'] == id:
            s['name'] = data.get('name', s['name'])
            s['grade'] = data.get('grade', s['grade'])
            s['section'] = data.get('section', s['section'])
            return jsonify({"message": "Student updated successfully!", "student": s})
    return jsonify({"error": "Student not found"}), 404

# Delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    global students
    students = [s for s in students if s['id'] != id]
    return jsonify({"message": "Student deleted successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
