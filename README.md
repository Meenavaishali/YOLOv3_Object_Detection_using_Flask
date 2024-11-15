# YOLOv3_Object_Detection_using_Flask


This project implements an object detection microservice with two main components: a UI backend service and an AI backend service. The UI allows users to upload images, and the AI backend performs object detection using the YOLOv3 model, returning results in JSON format. The components are containerized using Docker and deployed in a way that allows for easy setup and scalability.

## Table of Contents
- Overview
- Prerequisites
- Setup Instructions
- Docker Hub Setup
- Project Structure
- Usage
- Deliverables
- References
- Conclution

## Overview

This microservice leverages a lightweight object detection model (YOLOv3) to identify objects in an uploaded image. The model processes the image, detects objects, and returns results as bounding boxes and structured JSON output. The project is containerized using Docker, making deployment and replication straightforward.

## Prerequisites

To replicate and run this solution, ensure the following are installed on your system:

- **Docker**: Used to containerize the application for easy setup and deployment. [Docker Installation Guide](https://docs.docker.com/get-docker/)
- **Python**: Required to run the backend services.
- **Flask or FastAPI**: Used to build the UI and AI backend services.
- **YOLOv3 Object Detection Model**: We will use the YOLOv3 model for object detection. If you don't have GPU support, you can still run the model on a CPU.

For reference, you can use the [YOLOv3 repository](https://github.com/ultralytics/yolov3) by Ultralytics.

### Download YOLOv3 Model

To use YOLOv3 for object detection, follow these steps:

1. Go to the [YOLO website](https://pjreddie.com/darknet/yolo/).
2. Click on "yolov3.weights" to download the model weights.
3. Place the `yolov3.weights` file in the `ai_backend/model` folder in your project. [NOTE: As per git limit as 100 MB, Couldn't commit the file here]

In addition to the weights, you will also need the `yolov3.cfg` configuration file and the `coco.names` file, which contains class labels for the objects YOLO detects.

## Setup Instructions

1. **Clone or Download the Repository**:
   - Download this project folder or clone the repository.

2. **Install Docker**:
   - Follow the instructions for your OS to install Docker: [Docker Installation Guide](https://docs.docker.com/get-docker/).

3. **Build and Run Docker Containers**:
   - Navigate to the project directory and follow the instructions in the `docker-compose.yml` file to build and start the UI and AI services.

4. **Access the UI**:
   - Open your browser and go to `http://localhost:5000` to upload an image and view the detection results.

## Docker Hub Setup

1. **Create a Docker Hub Account**:
   - Go to [Docker Hub](https://hub.docker.com/) and create an account if you don’t have one.

2. **Create a Repository on Docker Hub**:
   - After logging in, create a new public or private repository named `yolov3_objectdetection`.

3. **Tag and Push Docker Image**:
   - After building the Docker image, tag it with your Docker Hub repository name.
   - Push the image to Docker Hub.

4. **Pulling the Image from Docker Hub** (Optional):
   - To use this image on another system, pull it directly from Docker Hub.

## Project Structure

```
├── README.md               # Project documentation
├── docker-compose.yml      # Docker Compose for managing services
├── ui_backend              # UI backend service (Flask or FastAPI)
│   └── app.py              # Main file for the UI service
|   └── templates           # Upload.html file
|   └── dockerfile          # Dockerfile for ui_backend container
|   └── requirements.txt    # Dependencies for UI backend (Flask)
├── ai_backend              # AI backend service for object detection
│   ├── detection.py        # Detection script using YOLO or other model
│   └── model               # Directory containing model files (e.g., yolov3.cfg, yolov3.weights, coco.names)
│   └── app.py              # AI backend service for object detection
|   └── output              # Folder to save output images and JSON results
|   └── dockerfile          # Dockerfile for ai_backend container
|   └── requirements.txt    # Dependencies for AI backend (Flask, OpenCV, YOLO)
```

## Usage

1. Upload an Image: In the UI, upload an image for object detection.
2. Receive JSON Response: The AI backend processes the image, detects objects, and returns a JSON response with detected objects' bounding boxes and confidence scores.
3. Output: The detected objects are highlighted with bounding boxes in the image, and the corresponding JSON response is saved in the `output` folder.

## Deliverables

When submitting the assignment, please provide:

1. A zipped project folder or a private GitHub repository link with clear documentation.
2. A step-by-step documentation of your approach, including references used.
3. Output images with bounding boxes and corresponding JSON files, saved in the `output` folder.

## References

- [YOLOv3 by Ultralytics](https://github.com/ultralytics/yolov3): Used as a reference model for object detection.
- [OpenCV Documentation](https://docs.opencv.org/): For image processing and handling bounding boxes.
- [YOLO Website](https://pjreddie.com/darknet/yolo/): Official YOLO website for downloading the YOLOv3 weights file.
