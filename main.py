from flask import Flask, Response,  redirect, url_for,render_template,request
import cv2
import face_recognition_app
import os
import base64
import json

#TODO create data just using csv is fine for registration, sdb movie, and access

app = Flask(__name__)

app.config['SERVER_NAME'] = '127.0.0.1:5000'  # Update with your specific server name

detection_complete = False
client_name=''
image_count = 0

UPLOAD_FOLDER = 'temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/capture', methods=['POST'])
def capture():
    global image_count
    image_count += 1

    # Parse the JSON data
    data = request.get_json()
    image_data = data.get('image_data')

    if image_data:
            # Remove the data URI prefix
            image_data = image_data.split(',')[1]

            # Add padding to the Base64 string to make it valid
            padding = '=' * (4 - (len(image_data) % 4))
            image_data += padding

            # Decode the base64-encoded image data
            img_bytes = base64.b64decode(image_data)

            # Save the image to a file
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.png')
            with open(image_filename, 'wb') as img_file:
                img_file.write(img_bytes)

            return 'Image captured and saved successfully'

    return 'No image data received'

def generate_frames():
    global detection_complete,client_name
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame,name = face_recognition_app.process_frame(frame)
        print(name)
        if name!='Unknown':
            detection_complete=True
            client_name=name.rsplit('.', 1)[0]
            # with app.app_context():
            #     return redirect(url_for('redirect_page'))
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    global detection_complete
    if detection_complete:
        return render_template('redirect_page.html')
    return render_template('index.html',detectionComplete=detection_complete)
    
@app.route('/exit_video_feed')
def exit_video_feed():
    return redirect(url_for('redirect_page'))
    
@app.route('/redirect_page')
def redirect_page():
    global client_name
    # Add code to display the page after the specific person is detected
    return render_template('redirect_page.html',name=client_name)
    
@app.route('/check_detection')
def check_detection():
    global detection_complete,client_name
    if detection_complete:
        return redirect(url_for('redirect_page',name=client_name))
    else:
        return "Detection not complete."

@app.route('/registration')
def registration():
    return render_template('user_form.html')

if __name__ == '__main__':
    app.run(debug=True)
