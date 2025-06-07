from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from ap_shadow_type_calculator import calculate_shadow_types, get_shadow_types_str

app = FastAPI()

@app.get("/shadow/{ap_type}/{subtype}")
async def get_shadow_json(ap_type: str, subtype: str):
    try:
        result_dict = calculate_shadow_types(ap_type, subtype)
        # Return as JSON response
        return JSONResponse(content=result_dict)
    except ValueError as e:
        return HTTPException(status_code=400, detail = e.args[0])

@app.get("/shadow.html/{ap_type}/{subtype}")
async def get_shadow_html(ap_type: str, subtype: str):
    try:
        shadow_types = calculate_shadow_types(ap_type, subtype)

        ap_type = shadow_types['ap_type']
        subtype = shadow_types["subtype"]
        results = [f'<h1>Shadow types for {ap_type} {subtype}:</h1><ol>']

        for shadow_type_and_description in shadow_types['shadow_types']:
            shadow_type = shadow_type_and_description['shadow_type']
            description = shadow_type_and_description["description"]
            results.append(f'<li>{shadow_type}: {description}</li>')
        results.append('</ol>')

        content = ''.join(results)
        return HTMLResponse(content=content)
    except ValueError as e:
        return HTTPException(status_code=400, detail = e.args[0])
