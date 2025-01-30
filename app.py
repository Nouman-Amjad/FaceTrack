from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import cv2
import numpy as np
import sqlite3
import pandas as pd
from ultralytics import YOLO
from keras_facenet import FaceNet

app = Flask(__name__)

# Load Models
yolo_model = YOLO("yolov8x-face-lindevs.pt").to("cpu")
facenet = FaceNet()

# Create directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

# Database setup
DATABASE = "database.db"
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, embedding_path TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, name TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

create_database()

def detect_faces(image_path):
    """ Detect faces using YOLOv8 """
    image = cv2.imread(image_path)
    results = yolo_model(image)
    boxes = []
    for result in results:
        for box in result.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = box
            boxes.append((int(x1), int(y1), int(x2), int(y2)))
    return boxes

def extract_faces(image_path, boxes):
    """ Extract and resize detected faces """
    image = cv2.imread(image_path)
    face_images = []
    for (x1, y1, x2, y2) in boxes:
        face = image[y1:y2, x1:x2]
        face_resized = cv2.resize(face, (160, 160))
        face_images.append(face_resized)
    return face_images

def get_face_embedding(face_image):
    """ Generate a FaceNet embedding from a face image """
    face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    face_array = np.expand_dims(face_rgb, axis=0)
    return facenet.embeddings(face_array)

def add_student_to_db(name, embedding):
    """ Save new student data to database """
    path = f"embeddings/{name}.npy"
    np.save(path, embedding)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, embedding_path) VALUES (?, ?)", (name, path))
    conn.commit()
    conn.close()

def recognize_face(face_embedding):
    """ Compare face embedding with stored embeddings """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, embedding_path FROM students")
    students = cursor.fetchall()
    conn.close()

    best_match = "Unknown"
    highest_similarity = 0.5  # Adjust threshold

    for name, emb_path in students:
        stored_embedding = np.load(emb_path)
        similarity = np.dot(face_embedding, stored_embedding.T) / (np.linalg.norm(face_embedding) * np.linalg.norm(stored_embedding))
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = name

    return best_match

def mark_attendance(name):
    """ Save attendance record """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        file = request.files["file"]
        path = f"uploads/{file.filename}"
        file.save(path)

        boxes = detect_faces(path)
        if not boxes:
            return "No face detected, please upload a valid face image.", 400

        faces = extract_faces(path, boxes)
        embedding = get_face_embedding(faces[0])
        add_student_to_db(name, embedding)

        return redirect(url_for("home"))
    return render_template("add_student.html")

@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance_page():
    if request.method == "POST":
        file = request.files["file"]
        path = f"uploads/{file.filename}"
        file.save(path)

        boxes = detect_faces(path)
        faces = extract_faces(path, boxes)

        image = cv2.imread(path)
        attendance_list = []

        for i, face in enumerate(faces):
            embedding = get_face_embedding(face)
            name = recognize_face(embedding)
            mark_attendance(name)  # Save to DB

            # Fetch timestamp
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT date FROM attendance WHERE name = ?", (name,))
            date = cursor.fetchone()
            conn.close()

            if date:
                attendance_list.append((name, date[0]))  # Ensure tuple format
            else:
                attendance_list.append((name, "No record found"))

            # Draw bounding box and name
            x1, y1, x2, y2 = boxes[i]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        labeled_path = "uploads/labeled_attendance.jpg"
        cv2.imwrite(labeled_path, image)

        return render_template("attendance_history.html", attendance_list=attendance_list, image_path=labeled_path)
    return render_template("mark_attendance.html")


@app.route("/attendance_history")
def attendance_history():
    """Fetch attendance records and render the improved history page."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch attendance records sorted by latest entry
    cursor.execute("SELECT name, date FROM attendance ORDER BY date DESC")
    attendance_list = cursor.fetchall()  # List of tuples [(name, date), (name, date), ...]
    conn.close()

    return render_template("attendance_history.html", attendance_list=attendance_list)


@app.route("/registered_students")
def registered_students():
    """Displays the list of registered students."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("registered_students.html", students=students)

@app.route("/clear_attendance", methods=["POST"])
def clear_attendance():
    """Deletes all attendance records from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance")
    conn.commit()
    conn.close()
    return redirect(url_for("attendance_history"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
