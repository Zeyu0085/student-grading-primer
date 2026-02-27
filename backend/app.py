from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception:
        return jsonify({"error": "not found"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if not name or not course or mark is None:
        return jsonify({"error": "name, course, and mark are required"}), 404
    
    student_data = db.insert_student(name, course, mark)
    return jsonify(student_data), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    name=student_data.get("name")
    course=student_data.get("course")
    mark=student_data.get("mark")

    student=db.get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "student not found"}), 404
    updated_student = db.update_student(student_id, name, course, mark)
    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student = db.get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "student not found"}), 404
    db.delete_student(student_id)
    return jsonify({"id": student_id}), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    data = db.get_all_students()
    count = len(data)
    if count == 0:
        return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200
    total = sum(student["mark"] for student in data)
    average = total / count if count > 0 else 0
    min_mark = min(student["mark"] for student in data) if data else 0
    max_mark = max(student["mark"] for student in data) if data else 0
    return jsonify({
        "count": count,
        "average": average,
        "min": min_mark,
        "max": max_mark
    }), 200
    


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
