from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pricing in INR per query
LLM_PRICING = {
    "GPT 4.0": {
        "Complex": 38.28,
        "Medium": 28.188,
        "Easy": 18.879
    },
    "GPT 4.0 Mini": {
        "Complex": 2.436,
        "Medium": 1.827,
        "Easy": 1.131  # based on your Excel logic
    }
}

# Input model for each user group
class UserGroup(BaseModel):
    num_users: int
    total_queries: int  # total daily queries directly given
    complex_pct: float
    medium_pct: float
    easy_pct: float
    llm_choice: str

# Main request input
class CalculationInput(BaseModel):
    user_groups: List[UserGroup]
    days_in_month: int = 30

# Cost calculation API
@app.post("/calculate_all_costs")
def calculate_all_costs(input: CalculationInput):
    results = []

    for group in input.user_groups:
        daily_queries = group.total_queries
        complex_daily = (daily_queries * group.complex_pct) / 100
        medium_daily = (daily_queries * group.medium_pct) / 100
        easy_daily = (daily_queries * group.easy_pct) / 100

        pricing = LLM_PRICING[group.llm_choice]

        # Daily cost calculations
        complex_cost_daily = complex_daily * pricing["Complex"]
        medium_cost_daily = medium_daily * pricing["Medium"]
        easy_cost_daily = easy_daily * pricing["Easy"]
        total_daily = complex_cost_daily + medium_cost_daily + easy_cost_daily

        # Monthly cost
        complex_monthly = complex_cost_daily * 20
        medium_monthly = medium_cost_daily * 20
        easy_monthly = easy_cost_daily * 20
        total_monthly = complex_monthly+medium_monthly+easy_monthly
        results.append({
            "LLM Model": group.llm_choice,
            "Total Users": group.num_users,
            "Daily Queries": daily_queries,
            "Complex Queries/Day": round(complex_daily, 2),
            "Medium Queries/Day": round(medium_daily, 2),
            "Easy Queries/Day": round(easy_daily, 2),
            "Cost/Complex Query": pricing["Complex"],
            "Cost/Medium Query": pricing["Medium"],
            "Cost/Easy Query": pricing["Easy"],
            "Daily Complex Cost": round(complex_cost_daily, 2),
            "Daily Medium Cost": round(medium_cost_daily, 2),
            "Daily Easy Cost": round(easy_cost_daily, 2),
            "Total Daily Cost": round(total_daily, 2),
            "Monthly Complex Cost": round(complex_monthly, 2),
            "Monthly Medium Cost": round(medium_monthly, 2),
            "Monthly Easy Cost": round(easy_monthly, 2),
            "Total Monthly Cost": round(total_monthly, 2)
        })

    return results
