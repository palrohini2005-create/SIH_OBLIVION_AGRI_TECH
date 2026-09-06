import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
import os

# ==============================
# SETTINGS
# ==============================

DATASET_PATH = "datasets"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10

# ==============================
# LOAD TRAINING DATA
# ==============================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# ==============================
# LOAD VALIDATION DATA
# ==============================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# ==============================
# GET CLASS NAMES
# ==============================

class_names = train_dataset.class_names

print("\nClasses:")
print(class_names)

# ==============================
# IMPROVE DATA LOADING
# ==============================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)

# ==============================
# DATA AUGMENTATION
# ==============================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])

# ==============================
# LOAD PRETRAINED MODEL
# ==============================

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

# ==============================
# CREATE OUR MODEL
# ==============================

model = models.Sequential([
    data_augmentation,

    layers.Rescaling(1./127.5, offset=-1),

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.2),

    layers.Dense(
        len(class_names),
        activation="softmax"
    )
])

# ==============================
# COMPILE MODEL
# ==============================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ==============================
# TRAIN MODEL
# ==============================

print("\nStarting training...\n")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)

# ==============================
# CREATE MODELS FOLDER
# ==============================

os.makedirs("models", exist_ok=True)

# ==============================
# SAVE MODEL
# ==============================

model.save("models/tomato_disease_model.keras")

print("\n==============================")
print("TRAINING COMPLETED!")
print("==============================")
print("Model saved at:")
print("models/tomato_disease_model.keras")