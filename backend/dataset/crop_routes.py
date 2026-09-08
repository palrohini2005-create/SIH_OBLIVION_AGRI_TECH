from flask import Blueprint, jsonify
from app.core.database import SessionLocal
from app.models import Crop

crop_bp = Blueprint("crop", __name__)


@crop_bp.route("/crops", methods=["GET"])
def get_crops():

    db = SessionLocal()

    try:
        crops = db.query(Crop).all()

        result = []

        for crop in crops:
            result.append({
                "crop_id": crop.crop_id,
                "crop_name": crop.crop_name
            })

        return jsonify(result)

    finally:
        db.close()