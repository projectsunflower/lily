# Project Lily - Automated Meter Reading

This project automates daily meter reading using M5STACK timer camera x (https://docs.m5stack.com/en/unit/timercam_x), M5STACK Flashlight (https://docs.m5stack.com/en/unit/FlashLight), Google Cloud services (Cloud Functions, Vision API, Firestore), and a Flask web application for visualization.

## Hardware Setup (M5Stack Cameras)

- Upload `main_water.cpp`, `main_gas.cpp`, `main_electricity.cpp` to each respective M5Stack device to capture images daily at 12:00 PM, triggering flashlight as needed.

## Google Cloud Platform Setup

### Cloud Function (`cloud_functions/main.py`)

- Deploy `process_meter_image` Cloud Function to process images from Google Cloud Storage, extract meter readings using Vision API, and store data in Firestore.

### Firestore Setup

- Create a Firestore database with a collection `meter_readings`.

### Vision API Setup

- Enable Google Cloud Vision API and set up service account key with necessary permissions.

## Flask Web Application Setup (`flask_app/`)

- Install dependencies: `pip install -r requirements.txt`
- Run Flask application locally: `python app.py`
- Access the web app at `http://localhost:8080` to view meter readings.

## Containerization and Deployment

### Docker Setup

- Build Docker image: `docker build -t your-image-name .`
- Run Docker container locally: `docker run -p 8080:8080 your-image-name`

### Cloud Build and Deployment to Cloud Run

- Set up Cloud Build trigger via GUI or CLI.
- Cloud Build will build the Docker image, push it to Container Registry, and deploy to Cloud Run automatically.

## Project Structure

root/
|– m5stack_camera/
|– cloud_functions/
|– flask_app/
|– Dockerfile
|– cloudbuild.yaml
|– README.md
|– requirements.txt


## Architecture

+---------------------+        +------------------+       +---------------------+
|    M5Stack Cameras   |  -->  |   Google Cloud   |  -->  |    Flask Web App    |
|   (Arduino Devices)  |       |   Storage (GCS)  |       |  (Google Cloud Run) |
+---------------------+        +------------------+       +---------------------+
        |                           |                            |
        | Image Capture & Upload    |                            |
        |-------------------------->|                            |
        |                           |                            |
        |                           | Image Processing (Cloud    |
        |                           | Function)                  |
        |                           |--------------------------->|
        |                           |                            |
        |                           |                            |
        |                           | Store Data (Firestore)     |
        |                           |<---------------------------|
        |                           |                            |
        |                           |                            |
        |                           | Display Readings           |
        |                           |--------------------------->|
        |                           |                            |
        |                           |                            |
        |                           | View Graphs and Readings   |
        |<--------------------------|                            |
+---------------------+       +------------------+       +---------------------+
|                     |       |                  |       |                     |
|    User Interface   |  <--  |   Vision API     |  <--  |     Firestore DB    |
|       (Browser)     |       |                  |       |                     |
+---------------------+       +------------------+       +---------------------+

Components Explained:

	1.	M5Stack Cameras (Arduino Devices):
	•	Arduino devices equipped with M5Stack capture images of water, gas, and electricity meters daily at 12:00 PM.
	2.	Google Cloud Storage (GCS):
	•	Images captured by M5Stack cameras are uploaded to GCS buckets (your_bucket_name) for storage and processing.
	3.	Cloud Function (Image Processing):
	•	A Cloud Function (process_meter_image) triggers on new image uploads to GCS. It uses Google Cloud Vision API to extract meter readings from images and stores the data in Firestore.
	4.	Firestore Database:
	•	Firestore is used to store meter readings (meter_readings collection) including meter type, reading values, and optionally kWh conversions for gas meters.
	5.	Flask Web Application (Google Cloud Run):
	•	A Flask web application deployed on Google Cloud Run (your-service-name) retrieves meter readings from Firestore and displays them to users. It includes functionality to visualize readings using graphs.
	6.	User Interface (Browser):
	•	Users interact with the Flask web application through a browser to view meter readings and graphs.

Key Interactions:

	•	Image Capture & Upload: M5Stack cameras capture images which are uploaded to GCS buckets.
	•	Image Processing: Cloud Function processes uploaded images, extracts meter readings using Vision API, and stores data in Firestore.
	•	Data Display: Flask web application retrieves meter readings from Firestore and presents them to users via a graphical interface.

Workflow:

	1.	Image Capture: M5Stack cameras capture meter images daily.
	2.	Upload to GCS: Images are uploaded to GCS buckets (your_bucket_name).
	3.	Image Processing: Cloud Function triggers on image upload, processes images using Vision API to extract meter readings, and stores results in Firestore.
	4.	Data Presentation: Flask web application fetches meter readings from Firestore, prepares graphical representations (graphs), and displays them to users.

This architecture diagram provides an overview of how your automated meter reading system integrates hardware (M5Stack cameras), cloud services (GCS, Cloud Functions, Vision API, Firestore), and a web application (Flask on Cloud Run) to automate and visualize meter readings effectively. Adjustments can be made based on specific requirements, such as adding additional functionalities or security measures as needed.


## Testing

Test Data Setup

	1.	Simulated Images for Upload:
	•	Create sample images that resemble meter readings for water, gas, and electricity meters. These images should contain clear and readable meter values.
	2.	Mock Firestore Data:
	•	Manually insert test data into Firestore for meter readings. This can be done using the Firestore console or programmatically using a script.

Steps to Test the Application

1. Testing M5Stack Camera Integration

	•	Objective: Ensure that M5Stack cameras capture images correctly and trigger uploads to Google Cloud Storage.
	•	Steps:
	•	Deploy the Arduino code (main_water.cpp, main_gas.cpp, main_electricity.cpp) to your M5Stack devices.
	•	Verify that each device captures an image at 12:00 PM (simulated time trigger).
	•	Check if the captured images are successfully uploaded to the specified GCS bucket (your_bucket_name).

2. Testing Cloud Function (Image Processing)

	•	Objective: Validate the Cloud Function’s ability to process uploaded images, extract meter readings using Vision API, and store data in Firestore.
	•	Steps:
	•	Upload simulated test images (water_meter_image.jpg, gas_meter_image.jpg, electricity_meter_image.jpg) to the GCS bucket.
	•	Monitor Cloud Function logs in the Google Cloud Console to ensure the function triggers upon image upload.
	•	Check Firestore to verify that meter readings (meter_readings collection) are stored correctly with accurate values extracted from images.

3. Testing Flask Web Application

	•	Objective: Verify that the Flask web application displays meter readings and graphs correctly based on data stored in Firestore.
	•	Steps:
	•	Start the Flask application locally using python app.py.
	•	Access the web application in a browser (http://localhost:8080).
	•	Verify that the Flask app fetches meter readings from Firestore and displays them on the UI.
	•	Check if graphs (using matplotlib or other plotting libraries) accurately represent the historical data trends for each meter type (water, gas, electricity).

4. End-to-End Integration Testing

	•	Objective: Test the entire workflow from image capture to data display in the Flask app.
	•	Steps:
	•	Simulate image capture by manually triggering the Arduino devices or modifying the Arduino code to trigger at shorter intervals for testing purposes.
	•	Monitor GCS for uploaded images and ensure Cloud Function processes them correctly.
	•	Verify that meter readings appear in Firestore and are updated in the Flask app without errors.
	•	Navigate through different pages or views in the Flask app to ensure all functionalities (graph display, numerical readings) work as expected.

Example Test Data

	•	Sample Images:
	•	water_meter_image.jpg: Simulated image of a water meter showing a reading.
	•	gas_meter_image.jpg: Simulated image of a gas meter showing a reading.
	•	electricity_meter_image.jpg: Simulated image of an electricity meter showing a reading.
	•	Mock Firestore Data:
	•	Insert test documents into meter_readings collection with fields:
	•	meter_type: water, gas, or electricity
	•	reading: Sample meter reading values
	•	reading_kwh (for gas): Calculated kWh equivalent


## Required Skills

	1.	Arduino Programming:
	•	Proficiency in programming with Arduino IDE or PlatformIO to interact with the ESP32 microcontroller. This includes understanding libraries, managing GPIO pins, and using hardware peripherals.
	2.	ESP32 and M5Stack:
	•	Familiarity with the ESP32 platform and specifically with M5Stack devices, including their features, libraries, and hardware setup.
	3.	Camera Integration:
	•	Understanding how to interface with a camera module (OV3660 in this case), including configuration of camera settings, capturing images, and handling image data in the microcontroller environment.
	4.	Network Communication:
	•	Knowledge of networking concepts, particularly WiFi communication and HTTP/HTTPS protocols for uploading data to cloud services (e.g., Google Cloud Storage).
	5.	Time Management:
	•	Ability to manage time using system time functions or an RTC module, ensuring accurate scheduling of tasks such as image capture at specific times (e.g., 12:00 PM).
	6.	Cloud Services Integration:
	•	Basic understanding of integrating with cloud services like Google Cloud Platform (GCP), including authentication, API usage, and potentially using services like Cloud Storage for storing captured images.
	7.	Troubleshooting and Debugging:
	•	Proficiency in debugging hardware and software issues, identifying and resolving common problems encountered during development.

## Experience Level

	•	Moderate to Advanced: This project requires a solid understanding of embedded systems, microcontroller programming, and interfacing with peripheral devices like cameras. Experience with similar IoT projects, especially those involving ESP32 or similar microcontrollers, would be beneficial.