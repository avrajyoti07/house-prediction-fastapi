import io
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse  # 1. FIX: Correct response import
from pydantic import BaseModel, Field

app = FastAPI()

model = joblib.load("house_model.joblib")
features = joblib.load("house_features.joblib")

# Input schema
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Media Income of Neighborhood") 
    HouseAge: float = Field(gt=0, description="Average Age of House in the block")
    AveRooms: float = Field(gt=0, description="Average Number of Rooms in the house")
    AveBedrms: float = Field(gt=0, description="Average Number of Bedrooms in the house")
    Population: float = Field(gt=0, description="Population of the block")
    AveOccup: float = Field(gt=0, description="Average Number of Occupants in the house")
    Latitude: float = Field(ge=-90, le=90, description="Latitude of the block")
    Longitude: float = Field(ge=-180, le=180, description="Longitude of the block")

@app.get("/")
def home():
    return {
        "message": "California House Price Prediction API is working",
        "status": "active",
        "endpoint": "send POST request to /predict"
    }

@app.get("/health")
def health():
    return {
        "status": "running",
        "model": "RandomForestRegressor",
        "features": features,
        "avg_error": "$32,000"
    }

@app.post("/predict")
def predict(house: HouseFeatures):
    try:
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])

        predicted = model.predict(input_data)[0]
        price_usd = predicted * 100000

        return {
            "predicted_price": f"${price_usd:,.0f}",
            "predicted_price_short": f"${predicted:,.2f} hundred thousands",
            "finance_range": f"${price_usd-32000:,.0f} to ${price_usd+32000:,.0f}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")
    
@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    try:
        contents = await file.read()
        
        # 2. FIX: Read byte contents using read_csv
        df = pd.read_csv(io.BytesIO(contents))

        required_columns = [
            "MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing_columns)}")
        
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")
        
        # 3. FIX: Compute and properly assign raw predictions scaled to USD
        predictions = model.predict(df[required_columns])
        df["Predicted_price_usd"] = predictions * 100000
        df["Predicted_price_usd"] = df["Predicted_price_usd"].apply(lambda x: f"${x:,.0f}")

        # 4. FIX: Convert DataFrame to an in-memory string buffer, then to a byte stream
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = io.BytesIO(stream.getvalue().encode("utf-8"))

        return StreamingResponse(
            response, 
            media_type="text/csv", 
            headers={"Content-Disposition": "attachment; filename=predictions.csv"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")