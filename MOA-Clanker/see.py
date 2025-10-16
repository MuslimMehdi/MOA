import cv2
import csv
import os
from datetime import datetime

# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def capture_face_images():
    # Initialize a dictionary to store faces with unique IDs
    faces_dict = {}

    # Set up a camera (0 is the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame using the cascade classifier
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate over each detected face
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Extract the face region from the original frame
            face_region = frame[y:y+h, x:x+w]

            # Convert the face to grayscale for facial feature extraction
            gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)

            # Check if the face is already in the dictionary
            unique_id = 0
            while unique_id in faces_dict:
                unique_id += 1

            # If not, add it to the dictionary with a new ID
            if gray_face not in faces_dict.values():
                faces_dict[unique_id] = {
                    'id': unique_id,
                    'image': gray_face.tostring(),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                print(f"Face {unique_id} detected!")

        # Display the frame with rectangles around each face
        cv2.imshow('Frame', frame)

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def store_faces():
    if not os.path.exists("faces.csv"):
        with open("faces.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "image", "timestamp"])
            writer.writeheader()

    faces_to_write = {}
    for face_id, face_data in faces_dict.items():
        if len(faces_to_write) >= 100: # store up to 100 faces
            break
        faces_to_write[face_id] = {
            'id': face_id,
            'image': face_data['image'],
            'timestamp': face_data['timestamp']
        }

    with open("faces.csv", "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "image", "timestamp"])
        writer.writerow(faces_to_write)

def load_faces():
    if os.path.exists("faces.csv"):
        faces_dict.clear()
        with open("faces.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                face_id = int(row["id"])
                image_data = bytes.fromhex(row['image'])
                timestamp = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                faces_dict[face_id] = {
                    'id': face_id,
                    'image': image_data,
                    'timestamp': timestamp
                }

# Call the functions to start capturing and storing faces, then load them
capture_face_images()
load_faces()