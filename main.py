from fastapi import FastAPI
from fuzzy_engine import DigitalMaturityAnalyzer
import uvicorn

app = FastAPI(title="Цифровая зрелость организаций")
analyzer = DigitalMaturityAnalyzer()

@app.post("/assess")
async def assess_maturity(data: dict):
    """API для оценки зрелости"""
    try:
        result = analyzer.assess(data['metrics'])
        return {"maturity_index": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/roadmap")
async def generate_roadmap(data: dict):
    """Генерация дорожной карты"""
    try:
        return analyzer.generate_roadmap(data['metrics'])
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)