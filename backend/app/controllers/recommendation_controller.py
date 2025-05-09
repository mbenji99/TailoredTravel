from fastapi import APIRouter, HTTPException
from services.recommendation_service import recommend_items

router = APIRouter()

@router.get("/recommendations/")
def get_recommendations(user_id: str, budget: float):
    try:
        recommendations = recommend_items(user_id, budget)
        return {"user_id": user_id, "budget": budget, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
