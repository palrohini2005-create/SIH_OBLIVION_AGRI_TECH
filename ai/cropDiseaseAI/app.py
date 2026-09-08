from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import numpy as np
from PIL import Image

from disease_info import disease_info
from disease_solution import disease_solution
from disease_symptoms import disease_symptoms
from risk_engine import calculate_environment_risk


# ==================================================
# CREATE FLASK APP
# ==================================================

app = Flask(__name__)

# Allow frontend/backend to communicate with this API
CORS(app)


# ==================================================
# LOAD TRAINED AI MODEL
# ==================================================

model = tf.keras.models.load_model(
    "models/tomato_disease_model.keras"
)


# ==================================================
# MODEL CLASS NAMES
# ==================================================

class_names = [
    "Tomato_Early_Blight",
    "Tomato_Healthy",
    "Tomato_Late_Blight",
    "Tomato_Septoria_Leaf_Spot"
]


# ==================================================
# CONNECT MODEL CLASSES TO DISEASE IDs
# ==================================================

class_to_id = {
    "Tomato_Early_Blight": "D007",
    "Tomato_Healthy": None,
    "Tomato_Late_Blight": "D008",
    "Tomato_Septoria_Leaf_Spot": "D009"
}


# ==================================================
# HOME ROUTE
# ==================================================

@app.route("/")
def home():

    return "Crop Disease AI API is running!"


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "OK",
        "message": "AI model is working"
    })


# ==================================================
# ANALYZE CROP IMAGE
# ==================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # ------------------------------------------------
    # CHECK IMAGE
    # ------------------------------------------------

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400


    file = request.files["image"]


    try:

        # ------------------------------------------------
        # GET ENVIRONMENTAL DATA
        # ------------------------------------------------

        # These default values are only for testing.
        # Later your backend can send actual values.

        temperature = float(
            request.form.get("temperature", 24)
        )

        humidity = float(
            request.form.get("humidity", 75)
        )


        # ------------------------------------------------
        # READ IMAGE
        # ------------------------------------------------

        image = Image.open(file).convert("RGB")


        # ------------------------------------------------
        # RESIZE IMAGE
        # ------------------------------------------------

        image = image.resize((224, 224))


        # ------------------------------------------------
        # CONVERT IMAGE TO NUMPY ARRAY
        # ------------------------------------------------

        image_array = np.array(image)


        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # ------------------------------------------------
        # AI PREDICTION
        # ------------------------------------------------

        predictions = model.predict(
            image_array,
            verbose=0
        )


        # Find highest probability class
        predicted_index = np.argmax(
            predictions[0]
        )


        predicted_class = class_names[
            predicted_index
        ]


        # Calculate confidence
        confidence = float(
            predictions[0][predicted_index] * 100
        )


        # ------------------------------------------------
        # CONFIDENCE LEVEL
        # ------------------------------------------------

        if confidence >= 80:

            confidence_level = "HIGH"

        elif confidence >= 60:

            confidence_level = "MEDIUM"

        else:

            confidence_level = "LOW"


        # ------------------------------------------------
        # GET DISEASE ID
        # ------------------------------------------------

        disease_id = class_to_id[
            predicted_class
        ]


        # ==================================================
        # ENVIRONMENTAL RISK
        # ==================================================

        environment = calculate_environment_risk(
            "Tomato",
            temperature,
            humidity
        )


        # ==================================================
        # HEALTHY TOMATO
        # ==================================================

        if disease_id is None:

            return jsonify({

                "crop": "Tomato",

                "prediction": predicted_class,

                "disease_id": None,

                "disease": "Healthy Tomato Leaf",

                "confidence": round(
                    confidence,
                    2
                ),

                "confidence_level":
                    confidence_level,

                "temperature":
                    temperature,

                "humidity":
                    humidity,

                "environment_risk":
                    environment["environment_risk"],

                "symptoms": [],

                "message":
                    "No disease-specific treatment is required."

            })


        # ==================================================
        # DISEASE INFORMATION
        # ==================================================

        info = disease_info.get(
            disease_id
        )


        # ==================================================
        # DISEASE SOLUTION
        # ==================================================

        solution = disease_solution.get(
            disease_id
        )


        # ==================================================
        # DISEASE SYMPTOMS
        # ==================================================

        symptoms = disease_symptoms.get(
            disease_id,
            []
        )


        # ==================================================
        # CREATE RESPONSE
        # ==================================================

        response = {

            "crop": "Tomato",

            "prediction": predicted_class,

            "disease_id": disease_id,

            "disease": info["disease"],

            "scientific_name":
                info["scientific_name"],

            "causal_agent":
                info["causal_agent"],

            "description":
                info["description"],

            "confidence":
                round(confidence, 2),

            "confidence_level":
                confidence_level,

            "temperature":
                temperature,

            "humidity":
                humidity,

            "environment_risk":
                environment["environment_risk"],

            "symptoms":
                symptoms
        }


        # ==================================================
        # ADD SOLUTION / ADVISORY
        # ==================================================

        if solution:

            response["solution_id"] = (
                solution["solution_id"]
            )

            response["remedy"] = (
                solution["remedy"]
            )

            response["treatment"] = (
                solution["treatment"]
            )

            response["precaution"] = (
                solution["precaution"]
            )

            response["prevention"] = (
                solution["prevention"]
            )


        # ==================================================
        # RETURN FINAL JSON
        # ==================================================

        return jsonify(response)


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )