from mongodb import db
from datetime import datetime


history_collection = db["analysis_history"]


def save_analysis(
    farmer_id,
    farmer_name,
    crop,
    disease,
    confidence,
    recommended_solution
):
    analysis = {
        "farmer_id": farmer_id,
        "farmer_name": farmer_name,
        "crop": crop,
        "disease": disease,
        "confidence": confidence,
        "recommended_solution": recommended_solution,
        "date": datetime.now()
    }

    result = history_collection.insert_one(analysis)

    print("✅ Analysis history saved!")
    print("History ID:", result.inserted_id)