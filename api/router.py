from fastapi import APIRouter, HTTPException, File, UploadFile
from .controller import validate_gs1_code
from .models import GS1Input

router = APIRouter()

@router.post("/cargar")
async def cargar_gs1_code(gs1_input: GS1Input):
    try:
        response = await validate_gs1_code(gs1_input.gs1_string)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cargar-archivo/")
async def cargar_archivo(file: UploadFile = File(...)):
    contents = await file.read() 
    gs1_string = contents.decode("utf-8") 
    print("Contenido recibido:", gs1_string)  
    return await validate_gs1_code(gs1_string)  
