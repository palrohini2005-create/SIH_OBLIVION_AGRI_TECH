from flask import Blueprint, jsonify

from app.database import SessionLocal
from app.models import User, AnalysisHistory, Crop, Disease

official_bp = Blueprint("official", __name__)


@official_bp.route("/official/farmers", methods=["GET"])
def get_all_farmers():

    db = SessionLocal()

    try:
        farmers = (
            db.query(User)
            .filter(User.role == "farmer")
            .all()
        )

        result = []

        for farmer in farmers:
            result.append({
                "id": farmer.id,
                "name": farmer.name,
                "email": farmer.email,
                "phone": farmer.phone,
                "district": farmer.district,
                "village": farmer.village,
                "state": farmer.state
            })

        return jsonify(result)

    finally:
        db.close()


@official_bp.route(
    "/official/farmer/<int:farmer_id>/history",
    methods=["GET"]
)
def get_farmer_history_for_official(farmer_id):

    db = SessionLocal()

    try:
        records = (
            db.query(
                AnalysisHistory,
                User,
                Crop,
                Disease
            )
            .join(User, AnalysisHistory.farmer_id == User.id)
            .join(Crop, AnalysisHistory.crop_id == Crop.crop_id)
            .join(Disease, AnalysisHistory.disease_id == Disease.disease_id)
            .filter(AnalysisHistory.farmer_id == farmer_id)
            .all()
        )

        result = []

        for history, farmer, crop, disease in records:

            result.append({
                "history_id": history.history_id,
                "farmer_id": farmer.id,
                "farmer_name": farmer.name,
                "district": farmer.district,
                "crop": crop.crop_name,
                "disease": disease.disease_name,
                "confidence": history.confidence,
                "analysis_date": (
                    history.analysis_date.isoformat()
                    if history.analysis_date
                    else None
                )
            })

        return jsonify(result)

    finally:
        db.close()