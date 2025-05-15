from fastapi import FastAPI
from pydantic import BaseModel
from math import ceil

app = FastAPI()

class VideoInput(BaseModel):
    video_length: float  # in minutes

@app.post("/calculate")
def calculate_costs(data: VideoInput):
    # Calculate LLM cost
    llm_cost = data.video_length * 52.2
    llm_yearly = llm_cost * 12
    
    # Calculate other costs
    vector_db = data.video_length * 0.23 + 2175
    vector_yearly = vector_db * 12
    
    storage = ceil(data.video_length * 75 / 1024) * 87 * 0.025
    storage_yearly = storage * 12
    
    agentic = 86.87 * 87
    agentic_yearly = agentic * 12
    
    # Calculate totals
    total_cloud = vector_db + llm_cost + storage + agentic
    total_prem = vector_db + llm_cost
    total_cloud_yearly = total_cloud * 12
    total_prem_yearly = total_prem * 12
    
    # Return rounded values without formulas
    return {
        "monthly_costs": {
            "vector_db": round(vector_db, 3),
            "llm": round(llm_cost, 3),
            "storage": round(storage, 3),
            "agentic_ai": round(agentic, 3)
        },
        "yearly_costs": {
            "vector_db": round(vector_yearly, 3),
            "llm": round(llm_yearly, 3),
            "storage": round(storage_yearly, 3),
            "agentic_ai": round(agentic_yearly, 3)
        },
        "totals": {
            "monthly_cloud": round(total_cloud, 3),
            "monthly_on_prem": round(total_prem, 3),
            "yearly_cloud": round(total_cloud_yearly, 3),
            "yearly_on_prem": round(total_prem_yearly, 3)
        }
    }