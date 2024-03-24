from flask import Flask, request, jsonify, render_template
import cv2
import os

app = Flask(__name__)
app.config['DEBUG'] = True

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Update the process_image function to return only the filename
def process_image(file_path):
    # Read the image
    image = cv2.imread(file_path)

    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a simple thresholding operation
    _, processed_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # Save the processed image with a new filename
    processed_image_filename = 'processed_' + os.path.basename(file_path)

    processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_image_filename)
    cv2.imwrite(processed_image_path, processed_image)

    return processed_image_filename


    return processed_image_filename


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the uploaded image
        processed_image_filename = process_image(file_path)

        # Return the processed image path
        return jsonify({'processed_image_path': processed_image_filename})



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
