# 🏠 House Price Prediction API

A machine learning-powered REST API built with **FastAPI** that predicts house prices based on property features. The model is trained using scikit-learn and served via a high-performance FastAPI backend with interactive Swagger documentation.

---

## 📌 Features

- Predict house prices instantly via a REST API endpoint
- Trained ML model saved with `joblib` for fast loading
- Interactive API docs available at `/docs` (Swagger UI)
- Clean project structure with separate scripts for training, exploration, and serving
- Lightweight and ready for local or cloud deployment

---

## 🗂️ Project Structure

```
house-prediction-fastapi/
│
├── main.py               # FastAPI app — defines the /predict endpoint
├── train.py              # ML model training script
├── explore.py            # Data exploration and analysis script
├── house_model.joblib    # Trained ML model (generated after running train.py)
├── house_features.joblib # Saved feature names/columns used during training
├── .gitignore            # Ignores venv, .pyc, .joblib files, etc.
└── README.md             # Project documentation
```

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| FastAPI | API framework |
| Uvicorn | ASGI server |
| scikit-learn | Machine learning model |
| joblib | Model serialization |
| Pydantic | Request data validation |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/avrajyoti07/house-prediction-fastapi.git
cd house-prediction-fastapi
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn scikit-learn joblib
```

### 4. Train the Model

Run this first to generate `house_model.joblib` and `house_features.joblib`:

```bash
python train.py
```

### 5. Start the API Server

```bash
uvicorn main:app --reload
```

The server will start at: `http://127.0.0.1:8000`

---

## 📖 API Usage

### Interactive Docs (Swagger UI)

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

You can test the `/predict` endpoint directly from the browser — no extra tools needed.

---

### Predict House Price — `POST /predict`

Send a POST request with the house features as JSON:

**Request Example:**

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "area": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "stories": 2,
    "parking": 1
  }'
```

> **Note:** The exact input fields depend on the features used during training. Check `/docs` for the full schema.

**Response Example:**

```json
{
  "predicted_price": 4250000.0
}
```

---

## 🧪 Data Exploration

To explore the dataset and understand feature distributions before training:

```bash
python explore.py
```

---

## 📦 .gitignore

The following are excluded from version control:

- `venv/` — virtual environment
- `__pycache__/` — Python cache
- `*.pyc` — compiled Python files
- `.DS_Store` — macOS system file
- `*.joblib` — trained model files (regenerated via `train.py`)

---

## 🙋‍♂️ Author

**Avrajyoti Kundu**
- GitHub: [@avrajyoti07](https://github.com/avrajyoti07)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
