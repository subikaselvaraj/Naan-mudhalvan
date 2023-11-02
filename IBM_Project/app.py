# Install necessary libraries: pip install Flask ibm-watson ibm-cloud-sdk-core

from flask import Flask, render_template, request
from ibm_watson import VisualRecognitionV4
from ibm_watson.visual_recognition_v4 import FileWithMetadata
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name)

# Replace with your actual API key and service URL
api_key = "YOUR_API_KEY"
service_url = "YOUR_SERVICE_URL"

authenticator = IAMAuthenticator(api_key)
visual_recognition = VisualRecognitionV4(
    version="2022-08-20",
    authenticator=authenticator
)
visual_recognition.set_service_url(service_url)

@app.route("/", methods=["GET", "POST"])
def index():
    caption = None
    if request.method == "POST":
        # Handle image upload
        if "image" not in request.files:
            return render_template("index.html", error="No file part")

        image = request.files["image"]

        if image.filename == "":
            return render_template("index.html", error="No selected file")

        try:
            # Use Visual Recognition to analyze the uploaded image
            response = visual_recognition.classify(
                images_file=FileWithMetadata(image)
            ).get_result()

            # Extract the top caption from the response
            top_class = response["images"][0]["classifiers"][0]["classes"][0]["class"]
            caption = f"AI-generated Caption: {top_class}"
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html", caption=caption)

if __name__ == "__main__":
    app.run(debug=True)
