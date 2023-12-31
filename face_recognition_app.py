import face_recognition
import cv2
import numpy as np
import os
import csv

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
known_face_encodings = []
known_face_names = []
process_this_frame = True
return_name='Unknown'

for image in os.listdir('faces'):
    face_image = face_recognition.load_image_file(f'faces/{image}')
    print(image)
    face_encoding = face_recognition.face_encodings(face_image)[0]

    known_face_encodings.append(face_encoding)
    known_face_names.append(image)
print(known_face_names)

def process_frame(frame):
    global process_this_frame, known_face_encodings, known_face_names,face_names,return_name
    nik=''
    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
    display_name=''
    # Display the results
    for name in face_names:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        cv2.rectangle(frame, (230, 420), (420, 370), (255, 255, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        with open('form_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)  # Create a CSV reader

            # Specify the value you want to find
            nik = name.replace(".jpg", "")
            
            # Loop through each row in the CSV file
            for row in reader:
                name2 = row['NIK']
                if name2 == nik:
                    display_name=row['Nama']
                    
                    
        cv2.putText(frame, display_name.split(' ', 1)[0], (250, 400), font, 1.0, (0, 0, 0), 1)
        return_name=display_name

    return frame, return_name,nik
