from fastapi import HTTPException
from .service import GS1EvaluatorService

class GS1Controller:
    @staticmethod
    def evaluate_code(code: str) -> dict:
        if not code:
            raise HTTPException(status_code=400, detail="El código GS1-128 no puede estar vacío")
        
        result = GS1EvaluatorService.evaluate_code(code)
        return {"code": code, "result": result}
