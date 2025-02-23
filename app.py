from flask import Flask, render_template, request, redirect, url_for
import os
from main import input_image

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Check if a file was uploaded
        if "image" not in request.files:
            return "No file uploaded!"
        
        file = request.files["image"]
        
        # Check if the file is empty
        if file.filename == "":
            return "No file selected!"
        
        # Save the uploaded file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        
        # Process the image using main.py
        result = input_image(file_path)
        
        # Render the result on the screen
        return render_template("index.html", result=result,image_url = file_path)
    
    # Render the upload form for GET requests
    return render_template("index.html", result=None)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)