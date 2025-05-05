import cv2
import dlib
import numpy as np
import face_recognition
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import datetime
import os

# Load emotion model and dlib predictor
emotion_model = load_model("emotion_detection_model.h5")
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

# EAR (Eye Aspect Ratio) function
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Load known faces if available
def load_known_faces():
    try:
        encodings = list(np.load("face_encodings.npy", allow_pickle=True))
        names = list(np.load("face_names.npy", allow_pickle=True))
    except:
        encodings, names = [], []
    return encodings, names

known_face_encodings, known_face_names = load_known_faces()

# Logging function
def log_login(name):
    with open("logins.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {name}\n")

# GUI setup
window = tk.Tk()
window.title("SmartEd Face System")
window.geometry("900x700")

video_label = tk.Label(window)
video_label.pack()

emotion_text = tk.Label(window, font=("Helvetica", 14))
emotion_text.pack()

canvas = tk.Canvas(window, width=300, height=30)
canvas.pack()

cap = cv2.VideoCapture(0)
current_frame = None
blinked = False

# Frame updater
def update_frame():
    global current_frame
    ret, frame = cap.read()
    if not ret:
        return
    current_frame = frame.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    window.after(10, update_frame)

# Registration function
def register_face():
    global current_frame
    name = simpledialog.askstring("Register", "Enter your name:")
    if name and current_frame is not None:
        rgb_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(name)
            np.save("face_encodings.npy", known_face_encodings)
            np.save("face_names.npy", known_face_names)
            messagebox.showinfo("Success", f"Registered {name}")
        else:
            messagebox.showwarning("No Face", "No face detected. Try again.")

# Emotion detection with bar
def display_emotion_and_bar(face_image):
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(gray, (48, 48))
    face = face.astype("float") / 255.0
    face = img_to_array(face)
    face = np.expand_dims(face, axis=0)
    preds = emotion_model.predict(face, verbose=0)[0]
    max_index = np.argmax(preds)
    label = emotion_labels[max_index]
    confidence = int(preds[max_index] * 100)

    emotion_text.config(text=f"{label}: {confidence}%")
    canvas.delete("bar")
    canvas.create_rectangle(0, 0, confidence * 3, 30, fill="green", tags="bar")

# Blink detection
def detect_blink_and_emotion():
    global current_frame, blinked
    if current_frame is None:
        window.after(500, detect_blink_and_emotion)
        return
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for rect in faces:
        shape = predictor(gray, rect)
        shape_np = np.array([[p.x, p.y] for p in shape.parts()])
        left_eye = shape_np[36:42]
        right_eye = shape_np[42:48]
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        if ear < 0.22:
            blinked = True
        x1, y1, x2, y2 = rect.left(), rect.top(), rect.right(), rect.bottom()
        face_img = current_frame[y1:y2, x1:x2]
        display_emotion_and_bar(face_img)
    window.after(500, detect_blink_and_emotion)

# Recognition and greeting
def start_system():
    def recognize():
        global blinked
        if not blinked:
            window.after(500, recognize)
            return
        rgb_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                idx = matches.index(True)
                name = known_face_names[idx]
                log_login(name)
                messagebox.showinfo("Login", f"Welcome, {name}!")
                return
        messagebox.showwarning("Not Found", "Face not recognized.")
    recognize()

# Buttons
tk.Button(window, text="Register", command=register_face, width=20, height=2).pack(pady=10)
tk.Button(window, text="Start System", command=start_system, width=20, height=2).pack(pady=10)

update_frame()
detect_blink_and_emotion()
window.mainloop()
cap.release()
