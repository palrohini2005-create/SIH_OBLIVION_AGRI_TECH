from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app import models

# Import your AI prediction function
from ai.cropDiseaseAI.predict import predict_disease_from_bytes

router = APIRouter(prefix="/api/scans", tags=["Scans"])

@router.post("/analyze")
async def analyze_leaf(
    farmer_id: int,
    crop_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Read uploaded image bytes
    image_bytes = await file.read()
    
    # 2. Pass bytes to AI model
    ai_result = predict_disease_from_bytes(image_bytes)
    disease_id = ai_result["disease_id"]
    confidence = ai_result["confidence"]

    # 3. Handle Healthy Leaf
    if disease_id is None:
        return {
            "prediction": ai_result["predicted_class"],
            "confidence": f"{confidence}%",
            "confidence_level": ai_result["confidence_level"],
            "status": "Healthy",
            "message": "Leaf appears healthy. No treatment needed."
        }

    # 4. Fetch details from database
    disease = db.query(models.Disease).filter(models.Disease.disease_id == disease_id).first()
    if not disease:
        raise HTTPException(
            status_code=404, 
            detail=f"Disease ID '{disease_id}' detected by AI was not found in database."
        )

    solutions = db.query(models.Solution).filter(models.Solution.disease_id == disease_id).all()
    symptoms = db.query(models.Symptom).filter(models.Symptom.disease_id == disease_id).all()

    # 5. Log transaction in AnalysisHistory
    history = models.AnalysisHistory(
        farmer_id=farmer_id,
        crop_id=crop_id,
        disease_id=disease_id,
        confidence=confidence,
        image_path=f"uploads/{file.filename}"
    )
    db.add(history)
    db.commit()

    # 6. Return combined JSON response
    return {
        "prediction": ai_result["predicted_class"],
        "confidence": f"{confidence}%",
        "confidence_level": ai_result["confidence_level"],
        "disease": {
            "disease_id": disease.disease_id,
            "disease_name": disease.disease_name,
            "scientific_name": disease.scientific_name,
            "description": disease.description
        },
        "symptoms": [s.symptom for s in symptoms],
        "solutions": [
            {
                "remedy": sol.remedy,
                "treatment": sol.treatment,
                "precaution": sol.precaution,
                "prevention": sol.prevention
            } for sol in solutions
        ]
    }