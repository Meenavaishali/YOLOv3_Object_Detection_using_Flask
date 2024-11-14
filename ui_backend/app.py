from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import base64
from io import BytesIO
from PIL import Image
import os
import json

app = Flask(__name__, template_folder="templates", static_folder="output")

@app.route('/')
def index():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get the uploaded image file
        file = request.files.get('image')
        if not file:
            return jsonify({"error": "No image file provided"}), 400

        # Extract file name without extension
        file_name = os.path.splitext(file.filename)[0]  # Get the name without the extension

        try:
            # Get the backend URL from the environment variable or fallback to localhost
            backend_url = os.getenv("BACKEND_URL", "localhost")

            # Use the dynamically obtained backend URL to make the request
            response = requests.post(f'http://{backend_url}:5001/', files={'image': file})

            response.raise_for_status()  # Check if request was successful
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to reach prediction service: {str(e)}"}), 500

        try:
            # Get the result as JSON
            result = response.json()
            img_base64 = result.get("image")
            detections = result.get("detections")

            # Check if detections or image data are missing
            if not img_base64 or not detections:
                error_msg = result.get("message", "No objects detected in the image.")
                return render_template('upload.html', error_msg=error_msg), 400
        except ValueError:
            return jsonify({"error": "Invalid JSON response from prediction service"}), 500

        # Define the path to 'ai_backend/output' and create it if running locally
        if not os.path.exists('../ai_backend/output'):
            os.makedirs('../ai_backend/output', exist_ok=True)

        try:
            # Save the detections as a JSON file in the 'output' directory in 'ai_backend'
            output_json_path = os.path.join('../ai_backend/output', f'{file_name}_detections.json')
            with open(output_json_path, 'w') as json_file:
                json.dump(detections, json_file, indent=4)
        except Exception as e:
            return jsonify({"error": f"Failed to save detection JSON: {str(e)}"}), 500

        # Return the base64 string back to the frontend for display
        return render_template('upload.html', img_base64=img_base64, file_name=file_name)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/output/<filename>')
def serve_output(filename):
    # Serve the processed image from the output folder
    return send_from_directory('./output', filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
