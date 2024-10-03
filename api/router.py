from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from .service import GS1EvaluatorService

router = APIRouter()

@router.post("/evaluate-gs1-file/")
async def evaluate_file(file: UploadFile = File(...)):
    """
    Evalúa múltiples códigos GS1-128 desde un archivo de texto.
    El archivo debe contener códigos separados por saltos de línea.
    """
    try:
        content = await file.read()
        file_content = content.decode('utf-8')  # Asegura que se procese como texto
        results = GS1EvaluatorService.evaluate_file(file_content)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el archivo: {e}")
