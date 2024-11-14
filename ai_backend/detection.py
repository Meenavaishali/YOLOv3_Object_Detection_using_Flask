# detection.py
import cv2
import numpy as np
import random

# Load YOLO
net = cv2.dnn.readNetFromDarknet('./model/yolov3.cfg', './model/yolov3.weights')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names from coco.names
with open("./model/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


# Detect objects
def detect_objects(image):
    # Convert the image to a blob
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Process the detections
    height, width = image.shape[:2]
    boxes = []
    confidences = []
    class_ids = []

    for output in outs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids


# Apply Non-Maximum Suppression (NMS)
def apply_nms(boxes, confidences, nms_threshold=0.4):
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=nms_threshold)
    return indices


# Draw bounding boxes with random colors
# Draw bounding boxes with random colors
def draw_bounding_boxes(image, boxes, confidences, class_ids, indices, class_names):
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = f"{class_names[class_ids[i]]}: {confidences[i]:.2f}"

        # Generate a random color for each object
        color = [random.randint(0, 255) for _ in range(3)]

        # Draw a bold bounding box by drawing multiple rectangles
        thickness = 4  # Set the thickness higher to make the bounding box bold
        for j in range(2):  # Draw twice for extra thickness
            cv2.rectangle(image, (x, y), (x + w, y + h), tuple(color), thickness - j)

        # Draw bold text by layering multiple copies of the text
        font_scale = 0.7  # Increase font scale for readability if needed
        font_thickness = 2  # Set the thickness to make the label text bold

        # Draw the label text in bold by layering multiple instances
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness + 1)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, tuple(color), font_thickness)
