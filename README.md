# 🏠 House Price Predictor AI Web App

An AI-powered web application that predicts California house prices using a trained machine learning model. Built with FastAPI and deployed on Render.

## 🎯 Features

- **Machine Learning Model**: Linear Regression trained on California housing dataset
- **FastAPI Backend**: RESTful API for price predictions
- **Free Cloud Hosting**: Deployed on Render (no credit card required)
- **Simple API**: Easy-to-use POST endpoint for predictions

## 🚀 Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model** (optional, included):
   ```bash
   python train_model.py
   ```

3. **Run the app**:
   ```bash
   python main.py
   ```

   The app will start at `http://localhost:10000`

## 📡 API Usage

### Prediction Endpoint

**Request**:
```bash
POST /predict
Content-Type: application/json

{
  "data": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
}
```

**Response**:
```json
{
  "prediction": 452500.0
}
```

### Data Format

The input `data` array contains 8 features (in order):
1. MedInc - Median income in block
2. HouseAge - Median house age in block
3. AveRooms - Average number of rooms
4. AveBedrms - Average number of bedrooms
5. Population - Block population
6. AveOccup - Average occupation
7. Latitude - Block latitude
8. Longitude - Block longitude

## 📁 Project Structure

```
house-price-api/
├── main.py              # FastAPI application
├── train_model.py       # Model training script
├── house_model.pkl      # Trained ML model
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🛠️ Technologies

- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning library
- **joblib**: Model serialization
- **uvicorn**: ASGI server
- **Render**: Cloud hosting platform

## 📊 Model Details

- **Algorithm**: Linear Regression
- **Dataset**: California Housing Dataset
- **Features**: 8
- **Training/Test Split**: 80/20
- **Random State**: 42

## 🌐 Deployment

Deployed on [Render](https://render.com) with:
- **Start Command**: `uvicorn main:app --host=0.0.0.0 --port=10000`
- **Runtime**: Python 3
- **Instance**: Free tier

## 📝 License

MIT License

## 👨‍💻 Author

Suraj M

## 🤝 Contributing

Feel free to fork this project and submit pull requests!
