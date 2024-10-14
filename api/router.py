from fastapi import APIRouter, File, UploadFile
from .controller import validate_gs1_code, validate_and_generate_report

router = APIRouter()

@router.post("/GS1-128/")
async def validate_codes(file: UploadFile = File(...)):
    contents = await file.read()
    codes = contents.decode("utf-8").splitlines()

    results = {}
    for code in codes:
        results[code] = validate_gs1_code(code)

    csv_report_path = await validate_and_generate_report(codes)

    return {
        "validation_results": results,
        "csv_report_path": csv_report_path
    }
