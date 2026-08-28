from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Real Estate Evaluation API", version="1.0")

class PropertyInput(BaseModel):
    title: str
    price_nok: float
    bra_sqm: float = Field(..., gt=0, description="Square meters must be greater than zero")
    municipality: str
    has_carport: bool

@app.post("/evaluate")
def evaluate_property(prop: PropertyInput):
    # Safe division since Pydantic already guarantees bra_sqm > 0
    sqm_price = prop.price_nok / prop.bra_sqm
    
    notes = []
    if prop.price_nok <= 3600000:
        notes.append("Excellent psychological entry price (under 3.6M NOK).")
    else:
        notes.append("Above target entry threshold.")
        
    if prop.has_carport:
        notes.append("Includes carport/storage value.")

    return {
        "property_title": prop.title,
        "calculated_sqm_price": round(sqm_price, 2),
        "entry_price_assessment": "Positive" if prop.price_nok <= 3600000 else "Neutral",
        "strategic_notes": notes
    }