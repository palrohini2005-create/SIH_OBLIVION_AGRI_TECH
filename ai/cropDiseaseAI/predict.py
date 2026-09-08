
import tensorflow as tf
import numpy as np

# Import disease information
from disease_info import disease_info

# Import solution/advisory information
from disease_solution import disease_solution


# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

model = tf.keras.models.load_model(
    "models/tomato_disease_model.keras"
)


# ==========================================
# 2. CLASS NAMES
# ==========================================

class_names = [
    "Tomato_Early_Blight",
    "Tomato_Healthy",
    "Tomato_Late_Blight",
    "Tomato_Septoria_Leaf_Spot"
]


# ==========================================
# 3. CONNECT AI CLASS TO DISEASE ID
# ==========================================

class_to_id = {
    "Tomato_Early_Blight": "D007",
    "Tomato_Healthy": None,
    "Tomato_Late_Blight": "D008",
    "Tomato_Septoria_Leaf_Spot": "D009"
}


# ==========================================
# 4. TEST IMAGE
# ==========================================

image_path = "test_images/test.jpg"


# ==========================================
# 5. LOAD IMAGE
# ==========================================

image = tf.keras.utils.load_img(
    image_path,
    target_size=(224, 224)
)

image_array = tf.keras.utils.img_to_array(image)

image_array = tf.expand_dims(image_array, 0)


# ==========================================
# 6. MAKE AI PREDICTION
# ==========================================

predictions = model.predict(
    image_array,
    verbose=0
)

predicted_index = np.argmax(predictions[0])

predicted_class = class_names[predicted_index]

confidence = predictions[0][predicted_index] * 100


# ==========================================
# 7. CONFIDENCE LEVEL
# ==========================================

if confidence >= 80:
    confidence_level = "HIGH"

elif confidence >= 60:
    confidence_level = "MEDIUM"

else:
    confidence_level = "LOW"


# ==========================================
# 8. GET DISEASE ID
# ==========================================

disease_id = class_to_id[predicted_class]


# ==========================================
# 9. DISPLAY AI RESULT
# ==========================================

print("\n==========================================")
print("       AI CROP DISEASE DETECTION")
print("==========================================")

print("Crop:", "Tomato")

print("Prediction:", predicted_class)

print("Confidence: {:.2f}%".format(confidence))

print("Confidence Level:", confidence_level)


# ==========================================
# 10. DISPLAY DISEASE INFORMATION
# ==========================================

if disease_id is not None:

    info = disease_info[disease_id]

    print("------------------------------------------")

    print("Disease ID:", disease_id)

    print("Disease:", info["disease"])

    print("Scientific Name:", info["scientific_name"])

    print("Causal Agent:", info["causal_agent"])

    print("Description:", info["description"])


    # ======================================
    # 11. DISPLAY SOLUTION / ADVISORY
    # ======================================

    if disease_id in disease_solution:

        solution = disease_solution[disease_id]

        print("------------------------------------------")
        print("SOLUTION / ADVISORY")
        print("------------------------------------------")

        print("Solution ID:", solution["solution_id"])

        print("Remedy:", solution["remedy"])

        print("Treatment:", solution["treatment"])

        print("Precaution:", solution["precaution"])

        print("Prevention:", solution["prevention"])

    else:

        print("------------------------------------------")
        print("No solution available for this disease.")


# ==========================================
# 12. HEALTHY LEAF
# ==========================================

else:

    print("------------------------------------------")

    print("Disease ID: N/A")

    print("Disease: Healthy Tomato Leaf")

    print("No disease-specific treatment is required.")


# ==========================================
# 13. END
# ==========================================

print("==========================================")