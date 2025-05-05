# SmartEd – Emotion-Based Face Attendance System

## Introduction

SmartEd is an intelligent, AI-powered attendance and emotion detection system designed to revolutionize student engagement tracking. By leveraging facial recognition, blink detection (for anti-spoofing), and real-time emotion analysis, SmartEd records not just who is present—but how they feel during classes. Through this innovative system, educators gain deep insights into student emotional patterns over time, enabling customized learning interventions based on mood and participation trends.

## Project Description

SmartEd merges facial recognition technology with emotional intelligence to provide a new-age solution for educational monitoring. Traditional attendance systems offer binary insights—present or absent. SmartEd goes further by observing emotional states such as happiness, confusion, sadness, or stress during lessons. This emotional mapping, stored along with attendance data, allows institutions to better understand student engagement, identify disinterest early, and adapt content delivery accordingly.

A robust Tkinter GUI ensures user-friendliness, while integrated anti-spoofing mechanisms (blink detection) uphold system integrity. All data is processed in real-time, with secure storage and detailed log reports for administrators or educators.

## Proposed Solution & Justification

SmartEd provides a futuristic alternative to outdated attendance methods. By combining deep learning, facial recognition, and emotion detection, it delivers a system that is:

- Secure – prevents misuse via real-time blink verification.
- Insightful – captures and logs student emotions during classes.
- Actionable – enables educators to tailor teaching methods to student mood and mental readiness.
- Scalable – suitable for classrooms, labs, or even remote learning environments.

This student-centric approach promotes not only academic tracking but emotional well-being—leading to more inclusive and productive learning experiences.

## Key Features

- Face Recognition: Identifies and authenticates students using facial data.
- Blink Detection (Anti-Spoofing): Validates live presence by monitoring natural eye blinks using Eye Aspect Ratio (EAR).
- Emotion Detection: Analyzes real-time emotions (happy, sad, neutral, angry, etc.) using a pre-trained CNN model.
- Emotion Insights Dashboard: Records emotional states over time for academic performance analysis.
- Tkinter GUI: Simplified visual interface to register, detect, and log faces/emotions.
- Attendance Log: Generates and saves logs with timestamps, student identity, and emotion summaries.
- Data Privacy: Local processing and optional encrypted logs ensure compliance with privacy guidelines.

## Usage

1. Clone the repository to your local machine.
2. Install the required libraries using the provided `requirements.txt` file.
3. Run the application using:

   ```bash
   python main.py
   ```

4. Face Registration:
   - Add new student entries using the "Register" button.

5. Face & Emotion Recognition:
   - Click “Start” to launch live face detection.
   - The system recognizes known faces and detects current emotional state.

6. View Logs:
   - Access saved logs under the `/logs` directory for attendance and emotion tracking.

## Output

- Successful login with student name and timestamp.
- Detected emotion displayed in both text and colored bar (visual confidence meter).
- Logs saved with date, time, emotion, and face identity.
- Aggregate data can be used to analyze emotional patterns by:
  - Periods / lectures
  - Days of the week
  - Subjects or environments

## Contact

For inquiries, suggestions, or collaborations, please contact:
**Aashiq Shareef**  
Email: aashiqshareefas@gmail.com 
