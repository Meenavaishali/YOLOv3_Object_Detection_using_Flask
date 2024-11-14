from flask import Flask, request, jsonify
import numpy as np
import cv2
import base64
from detection import detect_objects, apply_nms, draw_bounding_boxes, classes  # Ensure to import necessary methods

app = Flask(__name__)

@app.route("/", methods=["POST"])
def detect():
    try:
        # Get the uploaded image
        file = request.files['image']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)

        if img is None:
            return jsonify({"error": "Invalid image file"}), 400

        # Perform object detection
        try:
            boxes, confidences, class_ids = detect_objects(img)
        except Exception as e:
            return jsonify({"error": f"Object detection failed: {str(e)}"}), 500

        # Apply Non-Maximum Suppression (NMS)
        try:
            indices = apply_nms(boxes, confidences)
        except Exception as e:
            return jsonify({"error": f"NMS application failed: {str(e)}"}), 500

        if len(indices) == 0:  # No objects detected
            return jsonify({
                "message": "No objects detected",
                "detections": []
            })

        # Draw bounding boxes on the image
        try:
            draw_bounding_boxes(img, boxes, confidences, class_ids, indices, classes)
        except Exception as e:
            return jsonify({"error": f"Drawing bounding boxes failed: {str(e)}"}), 500

        # Convert the image to JSON serializable format (Base64 encoding)
        _, buffer = cv2.imencode('.jpg', img)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Prepare the detection results in JSON format
        detection_results = []
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            result = {
                "class": classes[class_ids[i]],
                "confidence": float(confidences[i]),
                "bounding_box": {
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h)
                }
            }
            detection_results.append(result)

        # Return both the base64 image and detection results in JSON format
        return jsonify({
            "image": img_base64,
            "detections": detection_results
        })

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
