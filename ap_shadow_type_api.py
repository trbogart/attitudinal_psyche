from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ap_shadow_type_calculator import calculate_shadow_types

app = FastAPI()

@app.get("/shadow/{ap_type}/{subtype}")
async def get_shadow(ap_type: str, subtype: str):
    result_dict = calculate_shadow_types(ap_type, subtype)
    # Return as JSON response
    return JSONResponse(content=result_dict)