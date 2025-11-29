from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import joblib
import json
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(
    title="House Price Predictor API",
    description="AI-powered API for predicting California house prices",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
model = joblib.load("house_model.pkl")

# Storage for prediction history
history_file = "prediction_history.json"

class Input(BaseModel):
    data: Optional[list] = [8.3252, 41.0, 6.98, 1.02, 322, 2.55, 37.88, -122.23]

# ==================== FASTAPI ENDPOINTS ====================

@app.post("/predict")
def predict(input: Input = Input()):
    """
    Make a house price prediction.
    Input: [median_income, house_age, avg_rooms, avg_bedrooms, population, avg_occupation, latitude, longitude]
    """
    try:
        pred = model.predict([input.data])
        prediction = float(pred[0])
        save_prediction(*input.data, prediction)
        return {
            "prediction": prediction,
            "unit": "$100,000s",
            "success": True
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": "loaded",
        "service": "House Price Predictor"
    }

@app.get("/history")
def get_history():
    """Get all predictions"""
    return {"predictions": load_prediction_history()}

@app.get("/stats")
def get_stats():
    """Get statistics about predictions"""
    history = load_prediction_history()
    if not history:
        return {"message": "No predictions yet"}
    predictions = [r["prediction"] for r in history]
    return {
        "total": len(predictions),
        "avg": sum(predictions) / len(predictions),
        "min": min(predictions),
        "max": max(predictions)
    }

@app.delete("/history")
def clear_history_endpoint():
    """Clear history"""
    if os.path.exists(history_file):
        os.remove(history_file)
    return {"message": "History cleared"}

@app.get("/")
def root():
    """Serve the HTML UI"""
    return FileResponse("index.html")


# ==================== UTILITY FUNCTIONS ====================

def save_prediction(median_income, house_age, avg_rooms, avg_bedrooms, population, avg_occupation, latitude, longitude, prediction):
    """Save prediction to history"""
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except:
            pass
    history.append({
        "timestamp": datetime.now().isoformat(),
        "features": {
            "median_income": median_income,
            "house_age": house_age,
            "avg_rooms": avg_rooms,
            "avg_bedrooms": avg_bedrooms,
            "population": population,
            "avg_occupation": avg_occupation,
            "latitude": latitude,
            "longitude": longitude
        },
        "prediction": float(prediction)
    })
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def load_prediction_history():
    """Load prediction history from file"""
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
