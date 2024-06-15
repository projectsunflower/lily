# Flask application for displaying meter readings for each meter type

from flask import Flask, render_template
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.route('/')
def index():
    meter_readings = {}

    # Query Firestore for meter readings
    readings_ref = db.collection('meter_readings').stream()
    for reading in readings_ref:
        data = reading.to_dict()
        meter_type = data['meter_type']
        reading_value = data['reading']
        if meter_type not in meter_readings:
            meter_readings[meter_type] = {'dates': [], 'readings': []}
        meter_readings[meter_type]['dates'].append(reading.id)
        meter_readings[meter_type]['readings'].append(reading_value)

    # Render template with meter readings
    return render_template('index.html', meter_readings=meter_readings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)