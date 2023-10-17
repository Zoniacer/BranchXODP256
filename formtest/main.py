from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def data_entry_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    name = request.form.get('name')
    email = request.form.get('email')

    # Save the form data to a database or process it as needed
    # For demonstration, we'll print it here
    print(f"Name: {name}, Email: {email}")

    # Capture and save the image
    if 'image' in request.files:
        image = request.files['image']

        if image.filename != '':
            # Save the image to the uploads directory
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            # Process the image if needed (e.g., resizing, cropping)
            # For example, you can use the Python Imaging Library (Pillow)
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            img.save(image_path)

    return redirect(url_for('data_entry_form'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Create the 'uploads' directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
