# The Cloud Function processes images uploaded to Google Cloud Storage, extracts meter readings using Vision API, and stores data in Firestore

import os
from google.cloud import firestore, vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_key.json'

db = firestore.Client()

# Conversion factor for gas meter reading to kWh (example value)
GAS_TO_KWH_CONVERSION_FACTOR = 11.8

def process_meter_image(data, context):
    bucket_name = data['bucket']
    file_name = data['name']
    meter_type = determine_meter_type(file_name)  # Extract meter type from file name

    vision_client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = f'gs://{bucket_name}/{file_name}'

    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    meter_value_str = texts[0].description.strip()
    meter_value = float(meter_value_str.replace(',', '.'))  # Handle different decimal separators

    # Convert gas meter reading to kWh if meter type is gas
    if meter_type == 'gas':
        meter_value_kwh = meter_value * GAS_TO_KWH_CONVERSION_FACTOR
    else:
        meter_value_kwh = None

    doc_ref = db.collection('meter_readings').document()
    doc_ref.set({
        'meter_type': meter_type,
        'reading': meter_value,
        'reading_kwh': meter_value_kwh  # Store kWh equivalent for gas meter
    })

    return f'Processed image {file_name} for {meter_type} meter'

def determine_meter_type(file_name):
    # Example: Extract meter type from file name
    if 'water' in file_name:
        return 'water'
    elif 'gas' in file_name:
        return 'gas'
    elif 'electricity' in file_name:
        return 'electricity'
    else:
        return 'unknown'