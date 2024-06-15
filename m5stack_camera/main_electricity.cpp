//# Arduino code for Electricity meter camera to capture image at 12:00pm and uploads it to Google Cloud Storage

#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
const char* gcsBucket = "your_bucket_name"; // Replace with your GCS bucket name
const char* gcsEndpoint = "https://storage.googleapis.com/your_bucket_name"; // Replace with your GCS endpoint

void setup() {
  Serial.begin(115200);
  delay(4000);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");
}

void loop() {
  // Check if it's 12:00 PM
  if (isTime12pm()) {
    captureImage("electricity");
  }

  delay(60 * 1000); // Check every minute
}

bool isTime12pm() {
    time_t now;
    struct tm timeinfo;

    // Get current system time
    time(&now);
    localtime_r(&now, &timeinfo);

    // Check if it's 12:00 PM (noon)
    if (timeinfo.tm_hour == 12 && timeinfo.tm_min == 0) {
        return true;
    } else {
        return false;
    }
}

void captureImage(String meterType) {
  HTTPClient http;
  http.begin(gcsEndpoint + "/" + meterType + "_meter_image.jpg");

  int httpResponseCode = http.POST(your_image_data); // Replace with actual image data
  if (httpResponseCode > 0) {
    Serial.print("Image uploaded successfully, HTTP response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error uploading image, HTTP response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}