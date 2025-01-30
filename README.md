# FaceTrack 🎭 - AI-Powered Face Recognition Attendance System  
🚀 **Automated attendance tracking using YOLOv8 & FaceNet**

## 📌 Features
✅ **Face Detection & Recognition** (YOLOv8 + FaceNet)  
✅ **Add New Students** with their face embeddings  
✅ **Mark Attendance** from classroom images  
✅ **View & Manage Attendance History** 📜  
✅ **Search & Filter Attendance Records** 🔍  
✅ **Labeled Attendance Images** for verification 🖼️  
✅ **Bootstrap UI for a clean & responsive design** 🎨  
✅ **Clear Attendance History (With Confirmation)** ❌  
✅ **Check Registered Students List** 📋  
✅ **Access the App from Any Device on Your Network** 🌍  

---

## 📸 Demo Screenshots  
### 🏠 Home Page  
<img src="static/screenshots/home.png" width="700">

### 🎭 Add New Student  
<img src="static/screenshots/add_student.png" width="700">

### 📜 Attendance History  
<img src="static/screenshots/attendance_history.png" width="700">

---

## ⚙️ Installation & Setup  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/FaceTrack.git
cd FaceTrack
```
### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
### **3️⃣ Run Flask Server**
```bash
python app.py
```
## 🌍 4️⃣ Access Web App

### **📌 Local Access**
Once the Flask server is running, open your browser and go to:
```bash
http://127.0.0.1:5000/
```
### **📌 Access from Another Device (Same Network)**
If you want to access the web app from a different device on the same network:
```bash
http://YOUR_LOCAL_IP:5000/
```

## 🏗️ Project Structure
```
📂 FaceTrack/
│── 📂 static/ # (CSS, JS, Images, Screenshots)
│── 📂 templates/ # HTML UI files
│ │── base.html # Navbar & Layout
│ │── index.html # Home Page
│ │── add_student.html # Register a new student
│ │── mark_attendance.html # Upload class image
│ │── attendance_history.html # View attendance records
│ │── registered_students.html # View enrolled students
│── 📂 uploads/ # Stores uploaded images (student/classroom)
│── 📂 embeddings/ # Stores face embeddings (.npy files)
│── app.py # Flask Backend (Main Application)
│── database.db # SQLite Database for attendance records
│── yolov8x-face-lindevs.pt # YOLOv8 Model for face detection
│── requirements.txt # Python dependencies file
│── README.md # Project Documentation
```
## 🎯 Usage
### **1️⃣ Add a Student**
- Navigate to **"Add Student"**.
- Upload a **clear face image** & enter the **name**.
- The system **stores the face embedding** for recognition.

### **2️⃣ Mark Attendance**
- Go to **"Mark Attendance"**.
- Upload a **classroom image** with multiple students.
- The system **detects & recognizes faces** and marks attendance.

### **3️⃣ View Attendance**
- Click **"View Attendance"**.
- **Search & Filter** records.
- See **labeled attendance images** for verification.

### **4️⃣ View Registered Students**
- Click **"Registered Students"** to see all enrolled names.

### **5️⃣ Clear Attendance (With Confirmation)**
- Click **"Clear Attendance"** on the history page.
- **Confirmation popup** prevents accidental deletion.

---

## 🎯 Roadmap (Upcoming Features)
✅ **Date-wise Attendance Filtering** 📅  
✅ **Export Attendance Reports (CSV, Excel, PDF)** 📂  
✅ **Generate Graphs & Attendance Analytics** 📊  
✅ **Real-Time Webcam Support for Live Attendance** 🎥  

---

## 🤝 Contributing
🚀 **Want to contribute? Follow these steps:**  
1. **Fork** this repository.  
2. **Create a branch** (`git checkout -b feature-branch`).  
3. **Commit changes** (`git commit -m "Added a new feature"`).  
4. **Push to GitHub** (`git push origin feature-branch`).  
5. **Create a Pull Request**.  

---

## 📜 License
This project is licensed under the **MIT License**. Feel free to use and modify.

---

## ⭐ Acknowledgments
- **YOLOv8** by Ultralytics for Face Detection.  
- **FaceNet** for Face Recognition.  
- **Flask** for Backend API.  
- **Bootstrap** for Modern UI.  

---

## ⭐ Support & Issues
💡 **Found an issue?** [Create an Issue](https://github.com/Nouman-Amajd/FaceTrack/issues).  
🎯 **Want new features?** Suggest them in **Discussions**.  
🚀 **Like this project?** Don’t forget to **Star ⭐ the Repo!**  

