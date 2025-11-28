from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import joblib
import gradio as gr
import json
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(title="House Price Predictor API")

# Load the trained model
model = joblib.load("house_model.pkl")

# Storage for prediction history
history_file = "prediction_history.json"

class Input(BaseModel):
    data: Optional[list] = [8.3252, 41.0, 6.98, 1.02, 322, 2.55, 37.88, -122.23]

# ==================== FASTAPI ENDPOINTS ====================

@app.post("/predict")
def predict(input: Input = Input()):
    """API endpoint for making predictions"""
    pred = model.predict([input.data])
    return {"prediction": pred[0]}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "model": "loaded"}

# ==================== UTILITY FUNCTIONS ====================

def save_prediction(median_income, house_age, avg_rooms, avg_bedrooms, 
                    population, avg_occupation, latitude, longitude, prediction):
    """Save prediction to history"""
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    
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
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

# ==================== GRADIO INTERFACE ====================

def make_prediction(median_income, house_age, avg_rooms, avg_bedrooms, 
                    population, avg_occupation, latitude, longitude):
    """Make a prediction and save to history"""
    features = [median_income, house_age, avg_rooms, avg_bedrooms, 
                population, avg_occupation, latitude, longitude]
    
    prediction = model.predict([features])[0]
    
    # Save to history
    save_prediction(median_income, house_age, avg_rooms, avg_bedrooms,
                   population, avg_occupation, latitude, longitude, prediction)
    
    return f"${prediction:.2f} (in $100,000s)"

def get_history_table():
    """Get formatted prediction history"""
    history = load_prediction_history()
    if not history:
        return "No predictions yet. Make a prediction to get started!"
    
    # Format as markdown table
    md_table = "| Date | Lat | Lon | Prediction |\n"
    md_table += "|------|-----|-----|-------------|\n"
    
    for record in history[-10:]:  # Show last 10
        timestamp = record["timestamp"][:10]  # Date only
        lat = record["features"]["latitude"]
        lon = record["features"]["longitude"]
        pred = record["prediction"]
        md_table += f"| {timestamp} | {lat:.2f} | {lon:.2f} | ${pred:.2f} |\n"
    
    return md_table

def get_statistics():
    """Get statistics about predictions"""
    history = load_prediction_history()
    if not history:
        return "No predictions yet."
    
    predictions = [r["prediction"] for r in history]
    avg_price = sum(predictions) / len(predictions)
    min_price = min(predictions)
    max_price = max(predictions)
    
    stats = f"""
    ### Prediction Statistics
    
    - **Total Predictions:** {len(predictions)}
    - **Average Price:** ${avg_price:.2f} (in $100,000s)
    - **Minimum Price:** ${min_price:.2f} (in $100,000s)
    - **Maximum Price:** ${max_price:.2f} (in $100,000s)
    - **Price Range:** ${max_price - min_price:.2f}
    """
    
    return stats

def clear_history():
    """Clear prediction history"""
    if os.path.exists(history_file):
        os.remove(history_file)
    return "✅ History cleared successfully!"

# ==================== BUILD GRADIO INTERFACE ====================

with gr.Blocks(title="House Price Predictor", theme=gr.themes.Soft()) as interface:
    gr.Markdown("# 🏠 House Price Predictor AI")
    gr.Markdown("*Predict California house prices using machine learning*")
    
    with gr.Tabs():
        # ===== HOME TAB =====
        with gr.TabItem("🏠 Home"):
            gr.Markdown("""
            ## Welcome to House Price Predictor!
            
            This AI application predicts California house prices based on:
            - **Median Income** in the area
            - **House Age** (median years)
            - **Average Rooms** per household
            - **Average Bedrooms** per household
            - **Population** density
            - **Average Occupation** level
            - **Geographic Location** (Latitude & Longitude)
            
            ### How it Works
            1. Go to the **Predict** tab
            2. Enter your house features
            3. Get an instant price prediction!
            4. Check the **History** tab to see all predictions
            
            ### About the Model
            - **Algorithm:** Linear Regression
            - **Dataset:** California Housing Dataset (1990)
            - **Accuracy:** Trained on 16,512 house records
            - **Features:** 8 input parameters
            
            ### Quick Example
            A house in San Francisco with:
            - Median Income: 8.33 (in $100,000s)
            - House Age: 41 years
            - Average Rooms: 6.98
            - Latitude: 37.88, Longitude: -122.23
            
            **Predicted Price:** ~$4.15 million (in 1990s value)
            """)
        
        # ===== PREDICT TAB =====
        with gr.TabItem("🎯 Predict"):
            gr.Markdown("### Enter House Features")
            
            with gr.Group():
                gr.Markdown("#### Location & Demographics")
                with gr.Row():
                    latitude = gr.Slider(32.5, 42.0, value=37.88, step=0.01, label="Latitude", info="32.5 - 42.0")
                    longitude = gr.Slider(-125.0, -114.0, value=-122.23, step=0.01, label="Longitude", info="-125 to -114")
                
                gr.Markdown("#### Economic Indicators")
                with gr.Row():
                    median_income = gr.Slider(0.5, 15.0, value=8.33, step=0.1, label="Median Income", info="in $100,000s")
                    population = gr.Number(value=1000, label="Population", info="Per block")
                
                gr.Markdown("#### Housing Characteristics")
                with gr.Row():
                    house_age = gr.Slider(1, 52, value=41, step=1, label="House Age (years)")
                    avg_rooms = gr.Slider(1.0, 15.0, value=6.98, step=0.1, label="Avg Rooms/Household")
                
                gr.Markdown("#### Additional Features")
                with gr.Row():
                    avg_bedrooms = gr.Slider(0.5, 5.0, value=1.02, step=0.05, label="Avg Bedrooms/Household")
                    avg_occupation = gr.Slider(1.0, 10.0, value=2.55, step=0.1, label="Avg Occupation")
            
            predict_btn = gr.Button("🔮 Predict Price", size="lg", variant="primary")
            prediction_output = gr.Textbox(label="Prediction Result", interactive=False)
            
            predict_btn.click(
                fn=make_prediction,
                inputs=[median_income, house_age, avg_rooms, avg_bedrooms, 
                       population, avg_occupation, latitude, longitude],
                outputs=prediction_output
            )
        
        # ===== HISTORY TAB =====
        with gr.TabItem("📊 History"):
            gr.Markdown("### Recent Predictions")
            
            with gr.Group():
                history_output = gr.Markdown("No predictions yet. Make a prediction to get started!")
                refresh_btn = gr.Button("🔄 Refresh History")
                
                refresh_btn.click(
                    fn=get_history_table,
                    outputs=history_output
                )
            
            # Auto-load history on tab open
            interface.load(get_history_table, outputs=history_output)
        
        # ===== STATISTICS TAB =====
        with gr.TabItem("📈 Statistics"):
            gr.Markdown("### Prediction Analytics")
            
            stats_output = gr.Markdown()
            refresh_stats_btn = gr.Button("🔄 Refresh Statistics")
            
            def update_stats():
                return get_statistics()
            
            refresh_stats_btn.click(fn=update_stats, outputs=stats_output)
            interface.load(update_stats, outputs=stats_output)
        
        # ===== ABOUT TAB =====
        with gr.TabItem("ℹ️ About"):
            gr.Markdown("""
            ## About House Price Predictor
            
            ### What is This?
            A machine learning web application that predicts California house prices 
            based on economic and geographic features.
            
            ### Technology Stack
            - **Framework:** FastAPI + Gradio
            - **ML Library:** scikit-learn
            - **Model:** Linear Regression
            - **Deployment:** Render
            
            ### Dataset Information
            - **Source:** California Housing Dataset (1990)
            - **Records:** 16,512 houses
            - **Features:** 8 numeric properties
            - **Target:** Median house value
            
            ### How Predictions Work
            1. You provide house features (location, age, rooms, etc.)
            2. The model processes your input
            3. Returns a predicted price based on patterns learned from 16,512 houses
            
            ### Model Accuracy
            - Trained on 80% of data (13,210 houses)
            - Tested on 20% of data (3,302 houses)
            - Uses Linear Regression algorithm
            
            ### Limitations
            - Model based on 1990 California data
            - May not reflect current 2024/2025 prices
            - Best for relative price comparisons
            - Assumes linear relationships between features
            
            ### Contact & Support
            - **Repository:** https://github.com/BytesofSurajm/house-price-api
            - **Deployment:** Render (Free Tier)
            - **API:** RESTful endpoints available
            
            ### Terms of Use
            This is a demonstration tool for educational purposes. 
            Predictions should not be used for actual real estate decisions.
            
            ---
            
            Built with ❤️ for learning AI and Machine Learning
            """)
        
        # ===== SETTINGS TAB =====
        with gr.TabItem("⚙️ Settings"):
            gr.Markdown("### System Settings")
            
            with gr.Group():
                gr.Markdown("#### Data Management")
                clear_btn = gr.Button("🗑️ Clear Prediction History", variant="stop")
                clear_output = gr.Textbox(label="Status", interactive=False)
                
                clear_btn.click(fn=clear_history, outputs=clear_output)
            
            with gr.Group():
                gr.Markdown("#### API Information")
                gr.Markdown("""
                **Base URL:** `/predict`
                
                **Method:** POST
                
                **Request Body:**
                ```json
                {
                  "data": [median_income, house_age, avg_rooms, avg_bedrooms, 
                           population, avg_occupation, latitude, longitude]
                }
                ```
                
                **Response:**
                ```json
                {"prediction": <house_price>}
                ```
                """)

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    import uvicorn
    import threading
    
    # Launch FastAPI on port 10000
    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=10000, log_level="info")
    
    # Run FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Launch Gradio interface
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
