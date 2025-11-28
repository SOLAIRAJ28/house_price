# 🎨 UI Documentation - House Price Predictor

## Overview

The House Price Predictor now features two complete user interfaces:

1. **Gradio Interface** - Python-based interactive UI
2. **HTML/CSS Interface** - Custom web interface

Both interfaces connect to the same FastAPI backend for predictions.

---

## 🎯 Gradio Interface

### Accessing the Gradio UI
```
URL: http://localhost:7860
```

### Pages Available

#### 1. 🏠 Home Page
- Welcome message and introduction
- Overview of the application
- Information about how it works
- Model details and accuracy metrics
- Quick example predictions

#### 2. 🎯 Predict Page
**Interactive form with sliders and number inputs:**

**Location & Demographics Section**
- `Latitude` - Slider (32.5 - 42.0)
- `Longitude` - Slider (-125 to -114)

**Economic Indicators Section**
- `Median Income` - Slider (0.5 - 15.0 in $100,000s)
- `Population` - Number input (per block)

**Housing Characteristics Section**
- `House Age` - Slider (1 - 52 years)
- `Average Rooms per Household` - Slider (1.0 - 15.0)

**Additional Features Section**
- `Average Bedrooms per Household` - Slider (0.5 - 5.0)
- `Average Occupation` - Slider (1.0 - 10.0)

**Features:**
- Real-time prediction on button click
- Clear, organized form layout
- Visual feedback with prediction results

#### 3. 📊 History Page
- Displays last 10 predictions in table format
- Shows: Date, Latitude, Longitude, Predicted Price
- Refresh button to update history
- Automatic loading on tab switch

#### 4. 📈 Statistics Page
- Overall prediction analytics
- Metrics displayed:
  - Total number of predictions made
  - Average predicted price
  - Minimum predicted price
  - Maximum predicted price
  - Price range

#### 5. ℹ️ About Page
- Detailed project information
- Technology stack explanation
- Dataset information
- Model accuracy details
- Limitations and disclaimers
- Contact and support information

#### 6. ⚙️ Settings Page
- Prediction history management
- Clear history button
- API documentation
- API endpoint details
- Example request/response formats

---

## 🌐 HTML/CSS Interface

### Accessing the HTML UI
```
URL: http://localhost:5000/static/index.html
OR open the index.html file in a web browser
```

### Features

**Modern Design:**
- Gradient purple theme
- Responsive design (works on mobile & desktop)
- Smooth animations and transitions
- Professional UI components

**Interactive Elements:**
- Range sliders with live value display
- Form validation
- Loading spinner during predictions
- Animated results display

### Pages Available

#### 1. 🏠 Home
- Welcome message
- How it works section
- Features analyzed list
- Model information card

#### 2. 🎯 Predict
**Advanced form with range sliders:**
- All input parameters with visual feedback
- Real-time value display as you adjust sliders
- Submit button with loading animation
- Result display with styled output

**Form Sections:**
- 📍 Location & Demographics
- 💰 Economic Indicators
- 🏘️ Housing Characteristics
- 🛏️ Additional Features

#### 3. 📊 History
- View past predictions
- Table format with filters
- Load history button
- Clear history option

#### 4. 📈 Statistics
- Prediction analytics
- Statistical summaries
- Data visualizations
- Performance metrics

#### 5. ℹ️ About
- Project purpose
- Technology stack details
- Dataset information
- Limitations and disclaimers
- External links

---

## 🔧 Technical Details

### Gradio Features

**Automatic Features:**
```python
- Auto-saving of prediction history
- Persistent storage in JSON format
- Automatic history loading on page visit
- Statistics calculation from stored data
```

**Components Used:**
```python
- gr.Blocks() - Main interface container
- gr.Tabs() - Tabbed interface
- gr.Slider() - Range input controls
- gr.Number() - Numeric inputs
- gr.Button() - Action buttons
- gr.Markdown() - Rich text content
- gr.Textbox() - Text display
- gr.Group() - Content grouping
```

### HTML/CSS Features

**Responsive Design:**
- Mobile-first approach
- CSS Grid layout
- Flexbox for components
- Media queries for breakpoints

**Styling:**
- Gradient backgrounds
- Shadow effects for depth
- Smooth transitions (0.3s)
- Hover effects on interactive elements

**JavaScript Functionality:**
```javascript
- Tab switching
- Form submission handling
- API communication
- Dynamic value updates
- Animation triggers
```

---

## 🚀 Starting the Application

### Option 1: Start with Gradio UI (Recommended)
```bash
python main.py
```

This starts:
- FastAPI server on port 10000
- Gradio UI on port 7860

Access at: `http://localhost:7860`

### Option 2: Start FastAPI Only
```bash
uvicorn main:app --host=0.0.0.0 --port=10000
```

Then access:
- API Docs: `http://localhost:10000/docs`
- Predictions: POST to `http://localhost:10000/predict`

### Option 3: Open HTML Interface
Simply open `index.html` in your web browser.

---

## 📊 Data Flow

```
User Input (UI)
    ↓
Form Validation
    ↓
API Request (POST /predict)
    ↓
FastAPI Backend
    ↓
Load Model
    ↓
Make Prediction
    ↓
Save to History
    ↓
Return Response
    ↓
Display Result (UI)
```

---

## 🎨 UI Customization

### Gradio Theme
Change the theme in `main.py`:
```python
interface = gr.Blocks(theme=gr.themes.Soft())
```

Available themes:
- `gr.themes.Soft()` - Current (soft colors)
- `gr.themes.Default()` - Default colors
- `gr.themes.Monochrome()` - Black & white
- `gr.themes.Glass()` - Frosted glass effect

### HTML/CSS Customization
Edit the `<style>` section in `index.html`:
```css
/* Change gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Modify fonts */
font-family: 'Your Font Name', sans-serif;

/* Adjust spacing */
padding: 40px;
```

---

## 🔗 API Integration

### Making a Prediction via API

**Using cURL:**
```bash
curl -X POST http://localhost:10000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]}'
```

**Using Python:**
```python
import requests

response = requests.post(
    'http://localhost:10000/predict',
    json={'data': [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]}
)
print(response.json())
```

**Using JavaScript (in HTML):**
```javascript
fetch('http://localhost:10000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        data: [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
    })
})
.then(response => response.json())
.then(data => console.log(data))
```

---

## 📝 Feature Input Guide

| Feature | Range | Description |
|---------|-------|-------------|
| Median Income | 0.5 - 15.0 | In $100,000s |
| House Age | 1 - 52 | Years |
| Avg Rooms | 1.0 - 15.0 | Rooms per household |
| Avg Bedrooms | 0.5 - 5.0 | Bedrooms per household |
| Population | 100 - 50000 | Per block |
| Avg Occupation | 1.0 - 10.0 | Numeric value |
| Latitude | 32.5 - 42.0 | °N |
| Longitude | -125 - -114 | °W |

---

## 🐛 Troubleshooting

### Gradio UI not loading
**Solution:** 
```bash
pip install -q gradio==4.20.1
python main.py
```

### API returning errors
**Check:**
- FastAPI is running on port 10000
- Model file exists: `house_model.pkl`
- All 8 features provided in correct format

### HTML interface not connecting to API
**Issue:** CORS policy
**Solution:** The API will handle CORS on Render automatically

### History not saving
**Check:**
- Write permissions in project directory
- `prediction_history.json` file created

---

## 🌐 Deployment Notes

### On Render
- Gradio UI will be available at your Render URL
- FastAPI endpoints accessible at `/api/*`
- HTML interface can be served as static file
- History persists in container (resets on redeploy)

### On Local Machine
- Both interfaces run simultaneously
- Port 10000 for FastAPI
- Port 7860 for Gradio
- No CORS issues locally

---

## 📈 Future Enhancements

Possible improvements:
- [ ] Add data visualization charts
- [ ] Implement user accounts for history
- [ ] Add model performance metrics dashboard
- [ ] Create mobile app
- [ ] Add dark mode toggle
- [ ] Implement batch predictions
- [ ] Add comparison tools
- [ ] Create API rate limiting

---

## 🎓 Learning Resources

- **Gradio Docs:** https://www.gradio.app/docs/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **scikit-learn:** https://scikit-learn.org/
- **HTML/CSS:** https://developer.mozilla.org/

---

**Built with ❤️ for learning AI and Machine Learning**
