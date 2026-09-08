from flask import Blueprint, jsonify, request

from app.core.database import SessionLocal
from app.models import (
    AnalysisHistory,
    User,
    Crop,
    Disease,
    Solution
)

history_bp = Blueprint("history", __name__)


# ==========================================
# GET FARMER HISTORY
# ==========================================

@history_bp.route("/farmer/<int:farmer_id>/history", methods=["GET"])
def get_farmer_history(farmer_id):

    db = SessionLocal()

    try:
        records = (
            db.query(
                AnalysisHistory,
                User,
                Crop,
                Disease,
                Solution
            )
            .join(User, AnalysisHistory.farmer_id == User.id)
            .join(Crop, AnalysisHistory.crop_id == Crop.crop_id)
            .join(Disease, AnalysisHistory.disease_id == Disease.disease_id)
            .outerjoin(
                Solution,
                AnalysisHistory.disease_id == Solution.disease_id
            )
            .filter(AnalysisHistory.farmer_id == farmer_id)
            .all()
        )

        result = []

        for history, user, crop, disease, solution in records:

            result.append({
                "history_id": history.history_id,

                "farmer": user.name,

                "crop": crop.crop_name,

                "disease": disease.disease_name,

                "scientific_name": disease.scientific_name,

                "confidence": history.confidence,

                "image_path": history.image_path,

                "remedy": solution.remedy if solution else None,

                "treatment": solution.treatment if solution else None,

                "precaution": solution.precaution if solution else None,

                "prevention": solution.prevention if solution else None,

                "analysis_date": (
                    history.analysis_date.isoformat()
                    if history.analysis_date
                    else None
                )
            })

        return jsonify(result)

    finally:
        db.close()


# ==========================================
# SAVE NEW ANALYSIS
# ==========================================

@history_bp.route("/analysis", methods=["POST"])
def save_analysis():

    data = request.get_json()

    farmer_id = data.get("farmer_id")
    crop_id = data.get("crop_id")
    disease_id = data.get("disease_id")
    confidence = data.get("confidence")
    image_path = data.get("image_path")

    db = SessionLocal()

    try:

        new_analysis = AnalysisHistory(
            farmer_id=farmer_id,
            crop_id=crop_id,
            disease_id=disease_id,
            confidence=confidence,
            image_path=image_path
        )

        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)

        return jsonify({
            "message": "Analysis saved successfully",
            "history_id": new_analysis.history_id
        }), 201

    finally:
        db.close()