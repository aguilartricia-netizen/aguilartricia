from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

# ----------------------------
# Dummy data (sample students)
# ----------------------------
students = [
    {"id": 1, "name": "Tricia Aguilar", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Cruz", "grade": 11, "section": "Genesis"},
    {"id": 3, "name": "Maria Santos", "grade": 12, "section": "Faith"}
]


# ----------------------------
# Home route
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html')



# ----------------------------
# GET all students
# ----------------------------
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "status": "success",
        "count": len(students),
        "students": students
    })


# ----------------------------
# GET one student by ID
# ----------------------------
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for s in students:
        if s['id'] == id:
            return jsonify({
                "status": "success",
                "student": s
            })
    return jsonify({"status": "error", "message": "Student not found"}), 404


# ----------------------------
# ADD a new student
# ----------------------------
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    # Basic validation
    if not data or not all(key in data for key in ("name", "grade", "section")):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    new_student = {
        "id": len(students) + 1,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    return jsonify({"status": "success", "message": "Student added!", "student": new_student}), 201


# ----------------------------
# UPDATE a student
# ----------------------------
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    for s in students:
        if s["id"] == id:
            s["name"] = data.get("name", s["name"])
            s["grade"] = data.get("grade", s["grade"])
            s["section"] = data.get("section", s["section"])
            return jsonify({"status": "success", "message": "Student updated!", "student": s})
    return jsonify({"status": "error", "message": "Student not found"}), 404


# ----------------------------
# DELETE a student
# ----------------------------
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    global students
    for s in students:
        if s["id"] == id:
            students = [st for st in students if st["id"] != id]
            return jsonify({"status": "success", "message": "Student deleted!"})
    return jsonify({"status": "error", "message": "Student not found"}), 404


# ----------------------------
# Run the app (local or deploy)
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)

