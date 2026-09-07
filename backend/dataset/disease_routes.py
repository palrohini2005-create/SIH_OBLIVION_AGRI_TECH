from flask import Blueprint, jsonify
from app.database import SessionLocal
from app.models import Disease

disease_bp = Blueprint("disease", __name__)


@disease_bp.route("/diseases/<disease_id>", methods=["GET"])
def get_disease(disease_id):

    db = SessionLocal()

    try:
        disease = db.query(Disease).filter(
            Disease.disease_id == disease_id
        ).first()

        if not disease:
            return jsonify({
                "error": "Disease not found"
            }), 404

        return jsonify({
            "disease_id": disease.disease_id,
            "crop_id": disease.crop_id,
            "crop_name": disease.crop_name,
            "disease_name": disease.disease_name,
            "scientific_name": disease.scientific_name,
            "causal_agent": disease.causal_agent,
            "description": disease.description
        })

    finally:
        db.close()