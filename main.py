from flask import Flask, Response,  redirect, url_for,render_template
import cv2
import face_recognition_app

app = Flask(__name__)

app.config['SERVER_NAME'] = '127.0.0.1:5000'  # Update with your specific server name

detection_complete = False
client_name=''

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
    print(10+detection_complete)
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



if __name__ == '__main__':
    app.run(debug=True)
