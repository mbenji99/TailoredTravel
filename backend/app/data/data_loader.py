# backend/app/api/recommendations.py
from fastapi import APIRouter
from backend.app.data.data_loader import load_all_data

router = APIRouter()

@router.get("/recommendations")
async def get_recommendations():
    # Load all datasets
    data = load_all_data()
    
    # Now, you can access the datasets like:
    trips_data = data['trips']
    tourism_stats_data = data['tourism_stats']
    travel_activity_data = data['travel_activity']
    hotels_data = data['hotels']
    
    # Your recommendation logic here
    recommendations = some_recommendation_function(trips_data, hotels_data)
    
    return {"recommendations": recommendations}
