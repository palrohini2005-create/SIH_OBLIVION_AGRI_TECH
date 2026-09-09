import io
import tensorflow as tf
import numpy as np
from PIL import Image

# Import disease information
from ai.cropDiseaseAI.disease_info import disease_info

# Import solution/advisory information
from ai.cropDiseaseAI.disease_solution import disease_solution

MODEL_PATH = "ai/cropDiseaseAI/models/tomato_disease_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# ==========================================
# 2. CLASS NAMES
# ==========================================

CLASS_NAMES = [
    "Tomato_Early_Blight",
    "Tomato_Healthy",
    "Tomato_Late_Blight",
    "Tomato_Septoria_Leaf_Spot"
]


# ==========================================
# 3. CONNECT AI CLASS TO DISEASE ID
# ==========================================

CLASS_TO_DISEASE_ID = {
    "Tomato_Early_Blight": "D007",
    "Tomato_Healthy": None,
    "Tomato_Late_Blight": "D008",
    "Tomato_Septoria_Leaf_Spot": "D009"
}

def predict_disease_from_bytes(image_bytes: bytes) -> dict:
    """Preprocesses raw image bytes, runs model inference,

    and returns the predicted metadata & mapped disease_id.
    """
    # 1. Load image from bytes and preprocess for Keras
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    image_array = tf.keras.utils.img_to_array(image)
    image_array = tf.expand_dims(image_array, axis=0)

    # 2. Run model inference
    predictions = model.predict(image_array, verbose=0)
    predicted_index = int(np.argmax(predictions[0]))

    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(predictions[0][predicted_index] * 100)

    # 3. Categorize confidence level
    if confidence >= 80:
        confidence_level = "HIGH"
    elif confidence >= 60:
        confidence_level = "MEDIUM"
    else:
        confidence_level = "LOW"

    # 4. Return minimal pure prediction result
    return {
        "crop": "Tomato",
        "predicted_class": predicted_class,
        "disease_id": CLASS_TO_DISEASE_ID[predicted_class],
        "confidence": round(confidence, 2),
        "confidence_level": confidence_level,
    }